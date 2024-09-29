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

import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class TaskExecutionContext:
    args: tuple[Any, ...]
    kwargs: dict[str, Any]


@dataclass(frozen=True)
class Success[T]:
    value: T


@dataclass(frozen=True)
class Failure:
    exc: str


@dataclass(frozen=True)
class TaskExecutionResult[T]:
    finished: bool = False
    value: T | None = None
    exc: str | None = None


@dataclass(frozen=True)
class TaskExecutable[**P, T]:
    name: str
    f: Callable[P, T] | Callable[P, Awaitable[T]]

    def execute(
        self, asyncio_runner: asyncio.Runner, *args: P.args, **kwargs: P.kwargs
    ) -> TaskExecutionResult[T]: ...  # pragma: nocover


@dataclass(frozen=True)
class SyncTaskExecutable[**P, T](TaskExecutable[P, T]):
    f: Callable[P, T]

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        return self.f(*args, **kwargs)

    def execute(
        self, asyncio_runner: asyncio.Runner, *args: P.args, **kwargs: P.kwargs
    ) -> TaskExecutionResult[T]:
        try:
            return TaskExecutionResult(finished=True, value=self(*args, **kwargs))
        except Exception as e:
            return TaskExecutionResult(finished=True, exc=repr(e))


@dataclass(frozen=True)
class AsyncTaskExecutable[**P, T](TaskExecutable[P, T]):
    f: Callable[P, Awaitable[T]]

    async def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        return await self.f(*args, **kwargs)

    def execute(
        self, asyncio_runner: asyncio.Runner, *args: P.args, **kwargs: P.kwargs
    ) -> TaskExecutionResult[T]:
        try:
            return TaskExecutionResult(
                finished=True, value=asyncio_runner.run(self(*args, **kwargs))
            )
        except Exception as e:
            return TaskExecutionResult(finished=True, exc=repr(e))
