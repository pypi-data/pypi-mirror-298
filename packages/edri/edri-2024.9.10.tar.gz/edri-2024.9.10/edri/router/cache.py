from dataclasses import dataclass, field
from datetime import datetime, timedelta
from logging import getLogger
from threading import Thread, Event as EventThreading
from time import sleep
from typing import List, Type, Dict, Optional, Generator
from uuid import UUID

from edri.config.setting import CACHE_TIMEOUT, CACHE_INFO_MESSAGE
from edri.dataclass.event import Event
from edri.dataclass.response import ResponseStatus


@dataclass
class CacheItem:
    event: Event
    time: datetime = field(default_factory=datetime.now)


class Cache:
    """
    A cache for temporarily storing events with functionality to append events,
    find events based on type and other criteria, periodically clean expired events,
    and maintain a list of the most recent events for specific needs.

    Attributes:
        items (List[CacheItem]): A list of CacheItem instances representing the cached events.
        logger (Logger): Logger instance for logging cache operations and statuses.
        cleaner (Thread): A background thread for periodically cleaning the cache of
                          expired items.
        cleaner_stop (EventThreading): An event flag used to signal the cleaner thread
                                       to stop.

    Methods:
        append(event: Event) -> datetime: Adds a new event to the cache.
        find(event_type: Type[Event], request: bool, from_time: Optional[datetime]) -> List[Event]:
            Searches for events in the cache that match the given criteria.
        clean(): Periodically removes expired events from the cache based on the
                 CACHE_TIMEOUT setting.
        last_events() -> Dict[int, str]: Retrieves the last events for specific identifiers.
        events_from(event_id: str) -> List[Event]: Gets all events following a specific event ID.
        quit(): Signals the cleaner thread to stop and waits for it to finish.
    """

    def __init__(self) -> None:
        """
        Initializes the Cache instance, starts the background cleaner thread, and
        sets up the necessary attributes for cache management.
        """
        self.items: List[CacheItem] = []
        self.logger = getLogger(__name__)
        self.cleaner = Thread(target=self.clean, daemon=True)
        self.cleaner_stop = EventThreading()
        self.cleaner.start()

    def __del__(self):
        """
        Ensures that the cleaner thread is properly stopped when the Cache instance is
        destroyed. This method sets the stop event for the cleaner thread to signal it
        to stop its operation, preventing potential resource leaks or dangling threads.
        """
        if self.cleaner_stop:
            self.cleaner_stop.set()

    def append(self, event: Event) -> datetime:
        """
        Adds a new event to the cache and returns the timestamp when the event was added.

        Parameters:
            event (Event): The event to be added to the cache.

        Returns:
            datetime: The timestamp when the event was added to the cache.
        """
        item = CacheItem(event)
        self.items.append(item)
        return item.time

    def find(self, event_type: Type[Event], request: bool, from_time: Optional[datetime]) -> List[Event]:
        """
        Finds events in the cache matching the specified type, request status, and time criteria.

        Parameters:
            event_type (Type[Event]): The type of event to search for.
            request (bool): Whether to search for events with a specific request status.
            from_time (Optional[datetime]): The starting time to search for events from. If None,
                                            all matching events are returned regardless of time.

        Returns:
            List[Event]: A list of events matching the specified criteria.
        """
        items = [item for item in self.items if isinstance(item.event, event_type) and (
                item.event.response is None or item.event.response.get_status() == ResponseStatus.NONE) == request]
        if from_time is not None:
            return [item.event for item in items if item.time >= from_time]
        else:
            return [item.event for item in items]

    def clean(self) -> None:
        """
        Background thread method to clean expired events from the cache based on the CACHE_TIMEOUT.
        """
        last_log_sent = datetime.now()
        delta = timedelta(seconds=CACHE_TIMEOUT)
        while not self.cleaner_stop.is_set():
            now = datetime.now()
            limit = now - delta
            self.items = [item for item in self.items if item.time > limit]
            if now - timedelta(seconds=CACHE_INFO_MESSAGE) >= last_log_sent:
                self.logger.info("Count of cached events: %s", len(self.items))
                last_log_sent = now
            sleep(1)

    def last_events(self) -> dict[UUID, str]:
        """
        Retrieves the last events for specific identifiers, useful for tracking the most recent
        state or activity.

        Returns:
            Dict[int, str]: A dictionary mapping identifiers to their last event keys.
        """
        return {item.event._switch.router_id: item.event._key for item in self.items if item.event._switch}

    def events_from(self, key: str) -> Generator[Event, None, None]:
        """
        Generates all events from the cache following a specific event ID.

        This method allows iterating over all events that occur after a given event,
        identified by its unique key. It is useful for retrieving events sequentially
        after a specific point.

        Parameters:
            key (str): The unique identifier key of the event to start from.

        Yields:
            Event: Events occurring after the specified event.
        """
        found = False
        for item in self.items:
            if found:
                yield item.event
                continue
            if item.event._key == key:
                found = True

    def quit(self) -> None:
        """
        Signals the cleaner thread to stop its operation and waits for it to finish, ensuring
        a graceful shutdown of the cache cleaning process.
        """
        self.cleaner_stop.set()
        self.cleaner.join()
