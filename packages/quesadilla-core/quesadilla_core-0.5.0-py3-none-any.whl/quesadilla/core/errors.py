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

from dataclasses import dataclass

import ulid


class QuesadillaException(Exception):
    def __str__(self) -> str:
        return ""


@dataclass()
class TaskQueueException(QuesadillaException):
    namespace: str
    task_queue_name: str

    def __str__(self) -> str:
        return (
            f"namespace={repr(self.namespace)}, "
            f"task_queue_name={repr(self.task_queue_name)}"
        )


@dataclass()
class UnknownTaskQueueNameError(TaskQueueException):
    pass


@dataclass()
class DuplicateTaskQueueNameError(TaskQueueException):
    pass


@dataclass()
class TaskNameException(TaskQueueException):
    task_name: str

    def __str__(self) -> str:
        return (
            f"namespace={repr(self.namespace)}, "
            f"task_queue_name={repr(self.task_queue_name)}, "
            f"task_name={repr(self.task_name)}"
        )


@dataclass()
class UnknownTaskNameError(TaskNameException):
    pass


@dataclass()
class DuplicateTaskNameError(TaskNameException):
    pass


@dataclass()
class TaskException(Exception):
    namespace: str
    task_queue_name: str
    task_name: str
    task_id: ulid.ULID

    def __str__(self) -> str:
        return (
            f"namespace={repr(self.namespace)}, "
            f"task_queue_name={repr(self.task_queue_name)}, "
            f"task_name={repr(self.task_name)}, "
            f"task_id={repr(self.task_id)}"
        )


class TaskAlreadyQueued(TaskException):
    pass


class TaskDoesNotExistError(TaskException):
    pass


class TaskDoesNotExistAnymoreError(TaskDoesNotExistError):
    pass
