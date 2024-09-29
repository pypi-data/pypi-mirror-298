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
import threading
from dataclasses import dataclass
from typing import Any, ClassVar

from quesadilla.connectors.basic_queues import BasicQueue
from quesadilla.connectors.in_memory.thread_safe import Queue
from quesadilla.core.task_metadata import SerializableTask

from quesadilla.runners.runners.base import BaseRunner
from quesadilla.runners.runners.protocol import Event
from quesadilla.runners.workloads.protocol import Executor, Workload


class Thread[T: Workload](threading.Thread, Executor[T]):
    def __init__(self, workload: T, *args: Any, **kwargs: Any) -> None:
        super().__init__(name=str(workload.id), *args, **kwargs)
        self.workload = workload

    def run(self) -> None:
        self.workload.main_loop()

    def close(self) -> None:
        self.workload.close()

    def stop(self) -> None:
        self.workload.stop()


@dataclass(frozen=True)
class MultithreadingRunner(BaseRunner):
    logger: ClassVar[logging.Logger] = logging.getLogger(
        "quesadilla.runners.multithreading"
    )

    def make_workload[T: Workload](self, workload: T) -> Executor[T]:
        return Thread(workload)

    def make_queue(self) -> BasicQueue[SerializableTask[Any]]:
        return Queue()

    def make_event(self) -> Event:
        return threading.Event()
