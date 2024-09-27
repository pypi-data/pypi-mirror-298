from collections import defaultdict
from multiprocessing import Queue
from multiprocessing.connection import Connection
from typing import Dict, Type, Optional, Set
from logging import getLogger

from edri.abstract import ManagerBase
from edri.dataclass.event import Event, shareable_events
from edri.dataclass.response import ResponseStatus
from edri.events.edri import router, group
from edri.events.edri.router import LastEvents
from edri.router import Cache, HealthChecker


class Router:
    """
    Manages routing of events between components within the system, handling subscriptions
    to events, distributing events to subscribed components, and managing health checks.

    Attributes:
        queue (Queue[Event]): A queue for receiving events to be routed.
        logger (Logger): Logger instance for logging routing operations and outcomes.
        connections (Dict[str, Connection]): A dictionary mapping component names to their connections.
        subscribed_requests (Dict[Type[Event], Set[Connection]]): A dictionary mapping event types to sets
                                                                   of connections subscribed to those event types for requests.
        subscribed_responses (Dict[Type[Event], Set[Connection]]): Similar to subscribed_requests, but for responses.
        connector_pipe (Connection): A special connection for the connector component, if any.
        cache (Cache): An instance of the Cache class for temporarily storing events.
        health_checker (HealthChecker): An instance of the HealthChecker class for monitoring
                                        component health.

    Methods:
        subscribe_connector(event: router.SubscribeConnector): Handles subscriptions for the connector component.
        subscribe(event: router.Subscribe) -> Optional[Connection]: Subscribes a component to an event type.
        unsubscribe(event: router.Unsubscribe): Unsubscribes a component from an event type.
        unsubscribe_pipe(pipe: Connection): Removes a component's subscriptions based on its connection.
        send_from(event: router.SendFrom): Sends cached events to subscribed components based on criteria.
        send(event: Event, connections: Set[Connection]): Distributes an event to subscribed components.
        run(): Starts the event routing process, handling incoming events and managing subscriptions.
        quit(): Gracefully shuts down the router, ensuring all resources are cleaned up properly.
    """

    def __init__(self, queue: "Queue[Event]", components: Set[ManagerBase]) -> None:
        """
        Initializes the Router with a queue for incoming events and a set of components
        to be monitored for health checks.
        """
        super().__init__()
        self.queue: "Queue[Event]" = queue
        self.logger = getLogger(__name__)
        self.connections: Dict[str, Connection] = {}
        self.subscribed_requests: Dict[Type[Event], Set[Connection]] = defaultdict(set)
        self.subscribed_responses: Dict[Type[Event], Set[Connection]] = defaultdict(set)
        self.connector_pipe: Connection = None  # type: ignore
        self.cache = Cache()
        self.health_checker = HealthChecker(self.queue, components)

    def _add_subscription(self, subscriptions: Dict[Type[Event], Set[Connection]], event_type: Type[Event], pipe: Connection) -> None:
        """
        Adds a subscription for a given event type and connection.
        """
        if event_type in subscriptions:
            subscriptions[event_type].add(pipe)
        else:
            subscriptions[event_type] = {pipe}

    def _remove_subscription(self, subscriptions: Dict[Type[Event], Set[Connection]], event_type: Type[Event], pipe: Connection) -> None:
        """
        Removes a subscription for a given event type and connection.
        """
        if event_type in subscriptions:
            subscriptions[event_type].discard(pipe)

    def subscribe(self, event: router.Subscribe) -> Optional[Connection]:
        """
         Registers a component for receiving events of a specific type.
         """
        # Every serialized object is different... this should enforce consistency
        saved_pipe = self.connections.get(event.name, None)
        if saved_pipe is not None:
            event.pipe = saved_pipe
        elif event.pipe is not None:
            self.connections[event.name] = event.pipe
        else:
            self.logger.error("Missing pipe in subscribe event!")
            return None

        if event.request:
            self._add_subscription(self.subscribed_requests, event.event_type, event.pipe)
        else:
            self._add_subscription(self.subscribed_responses, event.event_type, event.pipe)

        self.health_checker.component_add(event.name, event.pipe)
        if self.connector_pipe is not None:  # If switch connector is running, send him info about new request
            subscribed_new = router.SubscribedNew(event=event.event_type, request=event.request)
            self.connector_pipe.send(subscribed_new)

        event.response.set_status(ResponseStatus.OK)
        pipe = event.pipe
        event.pipe = None
        pipe.send(event)
        self.logger.debug("Subscribed for %s event: %s", event.name, event.event_type)
        return pipe

    def subscribed_all(self, event: router.SubscribedAll):
        event.response.demands = router.Demands(
            requests=set(k for k in self.subscribed_requests.keys() if k in shareable_events),
            responses=set(k for k in self.subscribed_responses.keys() if k in shareable_events))
        if event.pipe:
            self.connector_pipe = event.pipe
        else:
            self.logger.warning("Missing pipe in subscribe event!")
        event.pipe = None
        self.connector_pipe.send(event)

    def subscribe_connector(self, event: router.SubscribeConnector) -> None:
        """
        Registers the connector component for receiving specific types of events.
        """
        if not self.connector_pipe:
            self.logger.error("Connector component is not running!")
            return
        if event.request:
            self.subscribed_requests[event.event].add(self.connector_pipe)
        else:
            self.subscribed_responses[event.event].add(self.connector_pipe)

    def unsubscribe(self, event: router.Unsubscribe) -> None:
        """
        Removes a component's subscription for a specific event type.
        """
        self._remove_subscription(
            self.subscribed_requests if event.request else self.subscribed_responses,
            event.event_type,
            event.pipe
        )

    def unsubscribe_pipe(self, pipe: Connection) -> None:
        """
        Removes all subscriptions associated with a given connection.
        """
        self.logger.warning("Removing subscription for this connection: %s", pipe)
        for manager, connection in self.connections.items():
            if connection == pipe:
                del self.connections[manager]
                break

        for event, subscribers in self.subscribed_requests.items():
            self.subscribed_requests[event] = {subscriber for subscriber in subscribers if subscriber != pipe}

        for event, subscribers in self.subscribed_responses.items():
            self.subscribed_responses[event] = {subscriber for subscriber in subscribers if subscriber != pipe}

    def last_events(self, event: LastEvents) -> None:
        event.response.last_events = self.cache.last_events()
        self.connector_pipe.send(event)

    def send_from(self, event: router.SendFrom) -> None:
        """
        Sends events from the cache to subscribed components based on specified criteria.
        """
        if event.key:
            cached_events = self.cache.events_from(event.key)
        else:
            cached_events = [item.event for item in self.cache.items]
        self.logger.debug("Sending cached events: %s", len(cached_events))
        for cache_event in cached_events:
            if not cache_event.has_response():
                if self.connector_pipe in self.subscribed_requests[cache_event.__class__]:
                    self.logger.debug("Sending to switch: %s", cache_event)
                    event.response.event = cache_event
                    self.connector_pipe.send(event)
            else:
                if self.connector_pipe in self.subscribed_responses[cache_event.__class__]:
                    self.logger.debug("Sending to switch: %s", cache_event)
                    event.response.event = cache_event
                    self.connector_pipe.send(event)

    def send(self, event: Event, connections: Set[Connection]) -> None:
        """
        Distributes an event to all subscribed components.
        """
        time = self.cache.append(event)
        if not connections:
            self.logger.info("Event without subscriber: %s", event)
            return

        for connection in connections:
            if event._switch and event._switch.received and self.connector_pipe == connection:  # This supposes to stop event storm
                self.logger.debug("Event discarded: %s", event)
                continue  # pragma: no cover
            try:
                connection.send(event)
            except BrokenPipeError as e:
                self.logger.error("Broken pipe - %s", connection, exc_info=e)
                self.unsubscribe_pipe(connection)
                self.health_checker.restart_component(connection, time)

    def run(self) -> None:
        """
        Continuously processes incoming events, routing them according to subscriptions
        and managing system health checks.
        """
        self.logger.info("Router has started!")
        while True:
            event: Event = self.queue.get()
            self.logger.debug("<- %s", event)
            if not event.has_response():
                if isinstance(event, group.Router):
                    if isinstance(event, router.Subscribe):
                        pipe = self.subscribe(event)
                        if not pipe:
                            continue
                        for undelivered_event in self.cache.find(event.event_type, True, event.from_time):
                            self.logger.debug("Sending cached events: %s", undelivered_event)
                            try:
                                pipe.send(undelivered_event)
                            except BrokenPipeError as e:
                                self.logger.error("Broken pipe - %s", pipe, exc_info=e)
                                self.unsubscribe_pipe(pipe)
                    elif isinstance(event, router.Unsubscribe):
                        self.unsubscribe(event)
                    elif isinstance(event, router.SubscribedAll):
                        self.subscribed_all(event)
                    elif isinstance(event, router.SubscribeConnector):
                        self.subscribe_connector(event)
                    elif isinstance(event, router.LastEvents):
                        self.last_events(event)
                    elif isinstance(event, router.SendFrom):
                        self.send_from(event)
                    elif isinstance(event, router.HealthCheck):
                        self.health_checker.control_start()
                        self.send(event, self.subscribed_requests.get(event.__class__, set()))
                    else:
                        self.logger.info("Unknown event: %s", event)
                else:
                    self.send(event, self.subscribed_requests[event.__class__])
            else:
                if isinstance(event, group.Router):
                    if isinstance(event, router.HealthCheck):
                        if not event.response.name:
                            self.logger.error("Wrong health check response - missing 'name'")
                            continue
                        self.health_checker.control_result(event.response.name, event.response.get_status())
                    else:
                        self.logger.info("Unknown event with response: %s", event)
                else:
                    self.send(event, self.subscribed_responses[event.__class__])

    def quit(self) -> None:
        """
        Stops the router and performs necessary cleanup operations.
        """
        self.cache.quit()
