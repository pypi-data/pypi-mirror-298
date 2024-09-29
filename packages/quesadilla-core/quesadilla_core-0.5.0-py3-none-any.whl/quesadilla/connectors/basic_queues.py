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
from typing import Protocol

# this Protocol represents anything that has a FIFO-queue interface
# for internal use only, to unify some interfaces for Python builtins


class BasicQueue[T](Protocol):
    def get(self, timeout: float | None = None) -> T: ...  # pragma: nocover

    def put(self, v: T, timeout: float | None = None) -> None: ...  # pragma: nocover


class BaseQueue[T](BasicQueue[T]):
    class Empty(queue.Empty):
        pass

    class Full(queue.Full):
        pass
