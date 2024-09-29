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
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from functools import cached_property
from itertools import chain
from typing import Any, ClassVar, Self

import ulid
from quesadilla.connectors.basic_queues import BasicQueue
from quesadilla.core.task_metadata import SerializableTask
from quesadilla.core.task_queues import TaskQueue

from quesadilla.runners.runners.configs import RunnerConfig
from quesadilla.runners.runners.protocol import Event, Runner, RunnerLoggingExtras
from quesadilla.runners.workloads.brokers import Broker
from quesadilla.runners.workloads.protocol import Executor, Workload
from quesadilla.runners.workloads.workers import Worker


@dataclass(frozen=True)
class BaseRunner(Runner, metaclass=ABCMeta):
    task_queue: TaskQueue

    config: RunnerConfig = field(kw_only=True, default_factory=RunnerConfig)

    id: ulid.ULID = field(default_factory=ulid.ULID, init=False)

    stopped: Event = field(init=False, repr=False)

    workers: list[Executor[Worker]] = field(
        init=False, repr=False, default_factory=list
    )
    brokers: list[Executor[Broker]] = field(
        init=False, repr=False, default_factory=list
    )

    logger: ClassVar[logging.Logger]

    @cached_property
    def logging_extras(self) -> RunnerLoggingExtras:
        return {
            "runner_id": str(self.id),
        }

    def __post_init__(self) -> None:
        super().__setattr__("stopped", self.make_event())

        self.workers.extend(
            self.make_workload(
                Worker(
                    runner=self,
                    task_queue=self.task_queue,
                    stopped=self.make_event(),
                    closed=self.make_event(),
                    scheduled_tasks=self.make_queue(),
                    results=self.make_queue(),
                )
            )
            for _ in range(self.config.workers)
        )
        self.brokers.extend(
            self.make_workload(
                Broker(
                    runner=self,
                    task_queue=self.task_queue,
                    stopped=self.make_event(),
                    closed=self.make_event(),
                    worker_selector=self.config.worker_selector_class(
                        [executor.workload for executor in self.workers]
                    ),
                )
            )
            for _ in range(self.config.brokers)
        )

    def wait(self) -> None:
        self.stopped.wait()

    def signal(self, sig: int | None = None) -> None:
        if not self.stopped.is_set():  # pragma: nobranch
            s = signal.Signals(sig) if sig is not None else sig
            if s is not None:  # pragma: nobranch
                self.logger.warning(
                    f"Received signal {s.name}", extra=self.logging_extras
                )
            if s in frozenset(
                (signal.SIGTERM, signal.SIGINT, None)
            ):  # pragma: nobranch
                self.stopped.set()

    def __enter__(self) -> Self:
        if self.stopped.is_set():
            raise RuntimeError("This runner has already been run")

        self.logger.info("Runner starting...", extra=self.logging_extras)
        for executor in chain(self.brokers, self.workers):
            executor.start()

        return self

    def __exit__(self, *_: Any, **__: Any) -> None:
        self.logger.info("Runner stopping...", extra=self.logging_extras)

        # the order in which we stop executors is very important
        # first, we close both workers and brokers to stop accepting new work
        for executor in chain(self.workers, self.brokers):
            executor.close()
        # then we stop and join workers to flush all scheduled work
        for executor in self.workers:
            executor.stop()
        for executor in self.workers:
            executor.join()
        # finally, we stop and join brokers to send results to the connector
        for executor in self.brokers:
            executor.stop()
        for executor in self.brokers:
            executor.join()

        self.logger.info("Runner exited gracefully", extra=self.logging_extras)
        self.stopped.set()

    @abstractmethod
    def make_workload[T: (Workload)](self, workload: T) -> Executor[T]: ...

    @abstractmethod
    def make_queue(self) -> BasicQueue[SerializableTask[Any]]: ...

    @abstractmethod
    def make_event(self) -> Event: ...
