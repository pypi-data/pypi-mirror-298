from dataclasses import dataclass
from datetime import datetime, timedelta
from logging import getLogger
from multiprocessing import Queue
from multiprocessing.connection import Connection
from typing import Optional, Dict

from edri.abstract import ManagerBase
from edri.config.setting import HEALTH_CHECK_TIMEOUT
from edri.dataclass.event import Event
from edri.dataclass.response import ResponseStatus
from edri.events.edri.router import HealthCheck
from edri.events.edri.scheduler import Set as SchedulerSet
from edri.events.edri.store import Set as StoreSet


class HealthChecker:
    """
    Monitors and records the health status of components within the system, scheduling regular
    health checks and storing the results for analysis and system management.

    Attributes:
        router_queue (Queue): The messaging queue used to communicate with the scheduler and store.
        logger (Logger): Logger instance for logging health check operations and outcomes.
        state (Dict[str, Record]): A dictionary storing the health status records for each component.
        last_check (Optional[datetime]): The timestamp of the last initiated health check cycle.
        components (set[ManagerBase]): A set of component instances that are monitored by the HealthChecker.

    Methods:
        set_task(): Schedules the next health check operation using the system's scheduler.
        component_add(name: str, pipe: Connection): Adds a new component to the monitoring list.
        control_start(): Initiates a health check cycle, saving the current status of components.
        control_result(name: str, status: ResponseStatus): Records the result of a health check for a component.
        save_status(): Stores the current health status of all components in the system's store.
        restart_component(pipe: Connection, time: datetime): Attempts to restart a component based on its connection.
    """
    @dataclass
    class Record:
        """
        Represents the health status of a system component.

        Attributes:
            name (str): The name of the component.
            pipe (Connection): A connection object used for communicating with the component.
            definition (Optional[ManagerBase]): The class definition of the component, if available.
            timestamp (datetime): The timestamp of the last health check.
            status (Optional[int]): The health status returned by the component, typically aligning
                                    with HTTP status codes or custom application-defined codes.
            event (Optional[str]): Additional event or information about the component's health.
        """
        name: str
        pipe: Connection
        definition: Optional[ManagerBase] = None
        timestamp: datetime = datetime.now()
        status: Optional[int] = None
        event: Optional[str] = None

    def __init__(self, router_queue: "Queue[Event]", components: set[ManagerBase]) -> None:
        """
        Initializes the HealthChecker with a set of components to monitor and the queue for communication.
        """
        self.router_queue = router_queue
        self.logger = getLogger(__name__)
        self.state: Dict[str, HealthChecker.Record] = {}
        self.last_check: Optional[datetime] = None
        self.components = components
        self.set_task()

    def set_task(self) -> None:
        """
        Schedules the health check operation at a regular interval defined by HEALTH_CHECK_TIMEOUT.
        """
        scheduler_set = SchedulerSet(
            event=HealthCheck(),
            when=datetime.now() + timedelta(seconds=HEALTH_CHECK_TIMEOUT),
            repeat=timedelta(seconds=HEALTH_CHECK_TIMEOUT),
            identifier="HealthCheckerTask"
        )
        self.router_queue.put(scheduler_set)

    def component_add(self, name: str, pipe: Connection) -> None:
        """
        Registers a new component for health monitoring.
        """
        if name not in self.state:
            found = None
            for component in self.components:
                if component.name == name:
                    found = component
                    break
            self.state[name] = self.Record(name, pipe, found)
            self.logger.debug("Manager was added %s %s", name, pipe)

    def control_start(self) -> None:
        """
        Marks the start of a health check cycle, updating records and preparing for result collection.
        """
        self.save_status()
        self.last_check = datetime.now()

    def control_result(self, name: str, status: ResponseStatus) -> None:
        """
        Records the health check result for a specific component.
        """
        self.logger.debug("Add status record to %s - %s", name, status)
        record = self.state[name]
        record.timestamp = datetime.now()
        record.status = status.value

    def save_status(self) -> None:
        """
        Compiles and stores the health status of all monitored components.
        """
        store_set = StoreSet(name="health_check", value={})
        now = datetime.now()
        store_set.value["timestamp"] = now.isoformat()
        for name, record in self.state.items():
            if record.status is None:
                self.logger.debug("%s has not been checked yet", record.name)
                continue
            if (record.timestamp + timedelta(seconds=HEALTH_CHECK_TIMEOUT * 2)) < now:
                self.logger.warning("%s did not send a status message - last status %s - %s",
                                    record.name, record.status, record.event)
            else:
                store_set.value[name] = {
                    "status": record.status,
                    "message": record.event,
                }
        self.router_queue.put(store_set)

    def restart_component(self, pipe: Connection, time: datetime) -> None:
        """
        Attempts to restart a component that is not responding or is reported to have issues.
        """
        self.logger.warning("Restarting component")
        for name, component in self.state.items():
            if component.pipe == pipe:
                if component.definition:
                    component.definition.__class__(router_queue=self.router_queue, from_time=time).start()
                    self.logger.info("Component restarted")
                else:
                    self.logger.error("Component was found - definition was missing")
                del self.state[name]
                break
        else:
            self.logger.error("Component was not found")
