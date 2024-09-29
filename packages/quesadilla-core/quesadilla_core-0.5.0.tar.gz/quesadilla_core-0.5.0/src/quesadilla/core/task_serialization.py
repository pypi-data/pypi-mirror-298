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


import datetime
from typing import Any, TypedDict

import ulid


def from_timestamp(timestamp: float) -> datetime.datetime:
    return datetime.datetime.fromtimestamp(timestamp, tz=datetime.UTC)


def from_timestamp_or_none(timestamp: float | None) -> datetime.datetime | None:
    return from_timestamp(timestamp) if timestamp else None


def to_timestamp(dt: datetime.datetime) -> float:
    return dt.timestamp()


def to_timestamp_or_none(dt: datetime.datetime | None) -> float | None:
    return to_timestamp(dt) if dt else None


class SerializedTaskExecutionContext(TypedDict):
    args: tuple[Any]
    kwargs: dict[str, Any]


class SerializedTaskExecutionResult[T](TypedDict):
    finished: bool
    value: T | None
    exc: str | None


class SerializedTask[T](TypedDict):
    id: ulid.ULID
    namespace: str
    task_queue_name: str
    task_name: str
    execution_context: SerializedTaskExecutionContext
    execution_result: SerializedTaskExecutionResult[T]
    queued_at: float
    started_at: float | None
    finalized_at: float | None
