# noinspection PyProtectedMember
from multiprocessing.connection import Connection
from dataclasses import dataclass, field
from typing import Type

from edri.dataclass.event import Event
from edri.config.constant import ApiType


@dataclass
class Client:
    socket: Connection
    type: ApiType
    events: set[Type[Event]] = field(default_factory=set)
    parameters: dict[str, str] = field(default_factory=dict)
