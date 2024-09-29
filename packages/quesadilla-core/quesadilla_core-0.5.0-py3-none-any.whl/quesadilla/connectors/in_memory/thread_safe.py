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

import queue
from collections import defaultdict
from dataclasses import dataclass, field

from quesadilla.connectors.basic_queues import BaseQueue
from quesadilla.connectors.in_memory.base import (
    BufferType,
    InMemoryConnector,
    LedgerType,
)


@dataclass(frozen=True)
class Queue[T](BaseQueue[T]):
    q: queue.Queue[T] = field(default_factory=queue.Queue)

    def get(self, timeout: float | None = None) -> T:
        try:
            return self.q.get(block=True, timeout=timeout)
        except queue.Empty as e:
            raise self.Empty(*e.args) from e

    def put(self, v: T, timeout: float | None = None) -> None:
        self.q.put(v, block=True, timeout=timeout)


@dataclass(frozen=True)
class ThreadSafeInMemoryConnector(InMemoryConnector):
    buffer: BufferType = field(
        default_factory=lambda: defaultdict(lambda: defaultdict(Queue)),
        init=False,
        repr=False,
    )
    ledger: LedgerType = field(
        default_factory=lambda: defaultdict(lambda: defaultdict(dict)),
        init=False,
        repr=False,
    )
