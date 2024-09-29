# `quesadilla` - an elegant background task queue for the more civilized age
# Copyright (C) 2024 Artur Ciesielski <artur.ciesielski@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import multiprocessing.managers
import multiprocessing.queues
import queue
from dataclasses import dataclass, field
from typing import Any

from quesadilla.connectors.basic_queues import BaseQueue
from quesadilla.connectors.in_memory.base import (
    BufferType,
    InMemoryConnector,
    LedgerType,
)
from quesadilla.core.task_serialization import SerializedTask


@dataclass(frozen=True)
class Queue[T](BaseQueue[T]):
    q: multiprocessing.queues.Queue[T]

    def get(self, timeout: float | None = None) -> T:  # pragma: nocover
        # this function is excluded from coverage
        # because it's executed in a separate process
        try:
            return self.q.get(block=True, timeout=timeout)
        except queue.Empty as e:
            raise self.Empty(*e.args) from e

    def put(self, v: T, timeout: float | None = None) -> None:
        self.q.put(v, block=True, timeout=timeout)


@dataclass(frozen=True)
class ProcessSafeInMemoryConnector(InMemoryConnector):
    buffer: BufferType = field(init=False, repr=False)
    ledger: LedgerType = field(init=False, repr=False)

    object_manager: multiprocessing.managers.SyncManager = field(
        default_factory=multiprocessing.Manager,
        init=False,
        repr=False,
    )

    def __post_init__(self) -> None:
        object.__setattr__(self, "buffer", self.object_manager.dict())
        object.__setattr__(self, "ledger", self.object_manager.dict())

    def queue(self, serialized: SerializedTask[Any]) -> None:
        if not serialized["namespace"] in self.buffer:
            self.buffer[serialized["namespace"]] = self.object_manager.dict()
        if not serialized["task_queue_name"] in self.buffer[serialized["namespace"]]:
            self.buffer[serialized["namespace"]][serialized["task_queue_name"]] = Queue(
                self.object_manager.Queue()  # type: ignore
            )

        if not serialized["namespace"] in self.ledger:
            self.ledger[serialized["namespace"]] = self.object_manager.dict()
        if not serialized["task_queue_name"] in self.ledger[serialized["namespace"]]:
            self.ledger[serialized["namespace"]][
                serialized["task_queue_name"]
            ] = self.object_manager.dict()

        return super().queue(serialized)
