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

import json
import uuid
from typing import Any

import ulid

from quesadilla.core.task_serialization import SerializedTask


class TaskJSONEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, (ulid.ULID, uuid.UUID)):  # pragma: nobranch
            return str(o)
        return super().default(o)  # pragma: nocover


class TaskJSONDecoder(json.JSONDecoder):
    def __init__(self, **kwargs: Any):
        kwargs["object_hook"] = self.object_hook
        super().__init__(**kwargs)

    def object_hook(self, obj: Any) -> Any:  # type: ignore
        if isinstance(obj, (list, tuple)):
            return tuple(map(self.object_hook, obj))  # type: ignore

        if isinstance(obj, dict):
            return {k: self.object_hook(v) for k, v in obj.items()}  # type: ignore

        if isinstance(obj, str):
            try:
                return ulid.ULID.from_str(obj)  # type: ignore
            except ValueError:
                pass
            try:
                return uuid.UUID(obj)  # type: ignore
            except ValueError:
                pass

        return obj


class JSONConnectorMixin:
    @staticmethod
    def encode(o: Any) -> str:
        return json.dumps(o, cls=TaskJSONEncoder)

    @staticmethod
    def decode(o: str) -> SerializedTask[Any]:
        return json.loads(o, cls=TaskJSONDecoder)
