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

from collections.abc import MutableMapping
from dataclasses import dataclass, field
from typing import Any

import ulid

from quesadilla.connectors.basic_queues import BaseQueue, BasicQueue
from quesadilla.connectors.mixins import JSONConnectorMixin
from quesadilla.connectors.protocol import Connector
from quesadilla.core.errors import TaskAlreadyQueued
from quesadilla.core.task_serialization import SerializedTask

# this in-memory connector is designed for use in testing and prototyping

BufferEntryType = BasicQueue[ulid.ULID]
BufferQueueType = MutableMapping[str, BufferEntryType]
BufferType = MutableMapping[str, BufferQueueType]
LedgerEntryType = MutableMapping[ulid.ULID, str]
LedgerQueueType = MutableMapping[str, LedgerEntryType]
LedgerType = MutableMapping[str, LedgerQueueType]


@dataclass(frozen=True)
class InMemoryConnector(JSONConnectorMixin, Connector):
    buffer: BufferType = field(init=False, repr=False)
    ledger: LedgerType = field(init=False, repr=False)

    def queue(self, serialized: SerializedTask[Any]) -> None:
        if (
            serialized["id"]
            in self.ledger[serialized["namespace"]][serialized["task_queue_name"]]
        ):
            raise TaskAlreadyQueued(
                namespace=serialized["namespace"],
                task_queue_name=serialized["task_queue_name"],
                task_name=serialized["task_name"],
                task_id=serialized["id"],
            )

        self.ledger[serialized["namespace"]][serialized["task_queue_name"]][
            serialized["id"]
        ] = self.encode(serialized)
        self.buffer[serialized["namespace"]][serialized["task_queue_name"]].put(
            serialized["id"]
        )

    async def aqueue(self, serialized: SerializedTask[Any]) -> None:
        return self.queue(serialized)

    def find(
        self, namespace: str, task_queue: str, task_id: ulid.ULID
    ) -> SerializedTask[Any] | None:
        if (qt := self.ledger[namespace][task_queue].get(task_id)) is None:
            return None
        return self.decode(qt)

    async def afind(
        self, namespace: str, task_queue: str, task_id: ulid.ULID
    ) -> SerializedTask[Any] | None:
        return self.find(namespace, task_queue, task_id)

    def pull(self, namespace: str, task_queue: str) -> SerializedTask[Any] | None:
        try:
            task_id = self.buffer[namespace][task_queue].get(timeout=0.1)
            return self.decode(self.ledger[namespace][task_queue][task_id])
        except (BaseQueue.Empty, KeyError):
            return None

    def update(
        self,
        namespace: str,
        task_queue: str,
        serialized: SerializedTask[Any],
    ) -> None:
        self.ledger[namespace][task_queue][serialized["id"]] = self.encode(serialized)
