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

import random
from collections.abc import Iterable, Iterator
from dataclasses import InitVar, dataclass, field
from typing import Protocol, Self

from quesadilla.runners.workloads.workers import Worker


class WorkerSelector(Protocol):
    def __init__(self, collection: list[Worker]) -> None: ...  # pragma: nocover

    def select(self) -> Worker: ...  # pragma: nocover

    def all(self) -> Iterable[Worker]: ...  # pragma: nocover


@dataclass(frozen=True)
class RandomSelector(WorkerSelector):
    collection: list[Worker] = field(repr=False)

    def select(self) -> Worker:
        return random.choice(self.collection)  # nosec

    def all(self) -> list[Worker]:
        return self.collection


@dataclass(frozen=True)
class RoundRobinSelector(WorkerSelector):
    @dataclass(frozen=True)
    class CircularIterator[IT]:
        collection: Iterable[IT] = field(repr=False)
        current_iterator: Iterator[IT] = field(init=False, repr=False)

        def __post_init__(self) -> None:
            self.reset()

        def __iter__(self) -> Self:
            return self

        def __next__(self) -> IT:
            try:
                return next(self.current_iterator)
            except StopIteration:
                self.reset()
                return next(self.current_iterator)

        def reset(self) -> None:
            super().__setattr__("current_iterator", iter(self.collection))

    collection: InitVar[list[Worker]]
    iterator: CircularIterator[Worker] = field(init=False, repr=False)

    def __post_init__(self, collection: list[Worker]) -> None:
        super().__setattr__(
            "iterator",
            iter(RoundRobinSelector.CircularIterator(collection)),
        )

    def select(self) -> Worker:
        return next(self.iterator)

    def all(self) -> Iterable[Worker]:
        return self.iterator.collection
