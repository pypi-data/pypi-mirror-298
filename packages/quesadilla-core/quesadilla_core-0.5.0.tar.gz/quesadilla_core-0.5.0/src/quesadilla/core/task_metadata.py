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

from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from functools import cached_property

import ulid

from quesadilla.core.task_executables import TaskExecutionContext, TaskExecutionResult
from quesadilla.core.task_serialization import (
    SerializedTask,
    from_timestamp,
    from_timestamp_or_none,
    to_timestamp,
    to_timestamp_or_none,
)


@dataclass(frozen=True)
class BaseTaskMetadata[T]:
    execution_context: TaskExecutionContext = field(repr=False)
    execution_result: TaskExecutionResult[T] = field(
        default_factory=TaskExecutionResult
    )

    id: ulid.ULID = field(default_factory=ulid.ULID)

    queued_at: datetime.datetime = field(default=datetime.datetime.now(datetime.UTC))
    started_at: datetime.datetime | None = None
    finalized_at: datetime.datetime | None = None

    @cached_property
    def started(self) -> bool:
        return self.started_at is not None

    @cached_property
    def finalized(self) -> bool:
        return self.finalized_at is not None


@dataclass(frozen=True)
class SerializableTask[T](BaseTaskMetadata[T]):
    namespace: str = field(kw_only=True)
    task_queue_name: str = field(kw_only=True)
    task_name: str = field(kw_only=True)

    def serialize(self) -> SerializedTask[T]:
        return {
            "id": self.id,
            "namespace": self.namespace,
            "task_queue_name": self.task_queue_name,
            "task_name": self.task_name,
            "execution_context": {
                "args": self.execution_context.args,
                "kwargs": self.execution_context.kwargs,
            },
            "execution_result": {
                "finished": self.execution_result.finished,
                "value": self.execution_result.value,
                "exc": self.execution_result.exc,
            },
            "queued_at": to_timestamp(self.queued_at),
            "started_at": to_timestamp_or_none(self.started_at),
            "finalized_at": to_timestamp_or_none(self.finalized_at),
        }

    @staticmethod
    def deserialize[NT](serialized: SerializedTask[NT]) -> SerializableTask[NT]:
        return SerializableTask(
            id=serialized["id"],
            namespace=serialized["namespace"],
            task_queue_name=serialized["task_queue_name"],
            task_name=serialized["task_name"],
            execution_context=TaskExecutionContext(
                args=serialized["execution_context"]["args"],
                kwargs=serialized["execution_context"]["kwargs"],
            ),
            execution_result=TaskExecutionResult(
                finished=serialized["execution_result"]["finished"],
                value=serialized["execution_result"]["value"],
                exc=serialized["execution_result"]["exc"],
            ),
            queued_at=from_timestamp(serialized["queued_at"]),
            started_at=from_timestamp_or_none(serialized["started_at"]),
            finalized_at=from_timestamp_or_none(serialized["finalized_at"]),
        )
