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
import multiprocessing
import multiprocessing.context
import multiprocessing.managers
import multiprocessing.queues
import multiprocessing.synchronize
import signal
import time
from dataclasses import dataclass, field
from typing import Any, ClassVar

from quesadilla.connectors.basic_queues import BasicQueue
from quesadilla.connectors.in_memory.process_safe import Queue
from quesadilla.core.task_metadata import SerializableTask

from quesadilla.runners.runners.base import BaseRunner
from quesadilla.runners.runners.protocol import Event
from quesadilla.runners.workloads.protocol import Executor, Workload


class Process[T: Workload](multiprocessing.Process, Executor[T]):
    def __init__(self, workload: T, *args: Any, **kwargs: Any) -> None:
        super().__init__(name=str(workload.id), *args, **kwargs)
        self.workload = workload

    def run(self) -> None:  # pragma: nocover
        # this function is excluded from coverage
        # because it's executed in a separate process
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        signal.signal(signal.SIGTERM, signal.SIG_IGN)

        self.workload.main_loop()

    def close(self) -> None:
        self.workload.close()

    def stop(self) -> None:
        self.workload.stop()


@dataclass(frozen=True)
class MultiprocessingRunner(BaseRunner):
    object_manager: multiprocessing.managers.SyncManager = field(
        default_factory=multiprocessing.Manager,
        init=False,
        repr=False,
    )

    logger: ClassVar[logging.Logger] = logging.getLogger(
        "quesadilla.runners.multiprocessing"
    )

    def wait(self) -> None:
        # @hack: this is a workaround for a deadlock with multiprocessing.Event.wait
        while not self.stopped.wait(timeout=0.1):  # pragma: nobranch
            time.sleep(0.5)  # pragma: nocover

    def make_workload[T: Workload](self, workload: T) -> Executor[T]:
        return Process(workload)

    def make_queue(self) -> BasicQueue[SerializableTask[Any]]:
        return Queue(self.object_manager.Queue())  # type: ignore

    def make_event(self) -> Event:
        return self.object_manager.Event()
