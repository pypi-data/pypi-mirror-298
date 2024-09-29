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

from importlib import import_module

from quesadilla.cli.errors import (
    InvalidModulePathError,
    InvalidTaskQueueError,
    NotATaskQueueError,
)
from quesadilla.core.task_queues import TaskQueue


def task_queue_dotted_path(dotted_path: str) -> TaskQueue:
    module_path, object_name = dotted_path.split("::", maxsplit=1)

    try:
        match (attr := getattr(import_module(module_path), object_name)):
            case TaskQueue():
                return attr
            case _:
                raise NotATaskQueueError(dotted_path)
    except ModuleNotFoundError as e:
        raise InvalidModulePathError(module_path) from e
    except AttributeError as e:
        raise InvalidTaskQueueError(object_name) from e
