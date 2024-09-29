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

from functools import cached_property
from typing import Any, Protocol, Self

from quesadilla.runners.runners.logging import RunnerLoggingExtras


class Event(Protocol):
    def is_set(self) -> bool: ...  # pragma: nocover

    def set(self) -> None: ...  # pragma: nocover

    def wait(self, timeout: float | None = None) -> bool: ...  # pragma: nocover


class Runner(Protocol):
    @cached_property
    def logging_extras(self) -> RunnerLoggingExtras: ...  # pragma: nocover

    def wait(self) -> None: ...  # pragma: nocover

    def signal(self, sig: int | None = None) -> None: ...  # pragma: nocover

    def __enter__(self) -> Self: ...  # pragma: nocover

    def __exit__(self, *_: Any, **__: Any) -> None: ...  # pragma: nocover
