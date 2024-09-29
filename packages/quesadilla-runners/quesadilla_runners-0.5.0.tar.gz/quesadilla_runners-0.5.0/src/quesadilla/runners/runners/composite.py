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

import logging
import signal
import threading
from contextlib import ExitStack
from dataclasses import dataclass, field
from functools import cached_property
from typing import Any, ClassVar, Self

import ulid

from quesadilla.runners.runners.protocol import Event, Runner, RunnerLoggingExtras


class CompositeRunnerLoggingExtras(RunnerLoggingExtras):
    runners: list[RunnerLoggingExtras]


@dataclass(frozen=True)
class CompositeRunner(Runner):
    runners: list[Runner] = field(kw_only=True)

    id: ulid.ULID = field(default_factory=ulid.ULID, init=False)

    exit_stack: ExitStack = field(default_factory=ExitStack, init=False, repr=False)
    stopped: Event = field(
        kw_only=True, default_factory=threading.Event, init=False, repr=False
    )

    logger: ClassVar[logging.Logger] = logging.getLogger("quesadilla.runners.composite")

    @cached_property
    def logging_extras(self) -> CompositeRunnerLoggingExtras:
        return {
            "runner_id": str(self.id),
            "runners": [runner.logging_extras for runner in self.runners],
        }

    def wait(self) -> None:
        self.stopped.wait()

    def signal(self, sig: int | None = None) -> None:
        if not self.stopped.is_set():  # pragma: nobranch
            s = signal.Signals(sig) if sig is not None else sig
            if s in frozenset((signal.SIGTERM, signal.SIGINT)):  # pragma: nobranch
                for runner in self.runners:
                    runner.signal(sig)
                self.stopped.set()

    def __enter__(self) -> Self:
        if self.stopped.is_set():
            raise RuntimeError("This runner has already been run")

        self.logger.info("Runner starting...", extra=self.logging_extras)
        for runner in self.runners:
            self.exit_stack.enter_context(runner)

        return self

    def __exit__(self, *_: Any, **__: Any) -> None:
        self.logger.info("Runner stopping...", extra=self.logging_extras)
        self.exit_stack.close()
        self.logger.info("Runner exited gracefully", extra=self.logging_extras)
        self.stopped.set()
