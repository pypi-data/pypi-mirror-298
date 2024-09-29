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

from quesadilla.core.errors import QuesadillaException


class QuesadillaCLIException(QuesadillaException):
    pass


@dataclass()
class NotATaskQueueError(QuesadillaCLIException, ValueError):
    path: str


@dataclass()
class InvalidModulePathError(QuesadillaCLIException, ValueError):
    path: str


@dataclass()
class InvalidTaskQueueError(QuesadillaCLIException, ValueError):
    name: str
