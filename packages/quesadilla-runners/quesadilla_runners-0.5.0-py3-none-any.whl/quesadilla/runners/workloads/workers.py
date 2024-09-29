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


import asyncio
import logging
import time
from dataclasses import dataclass, field
from functools import cached_property
from typing import Any, ClassVar

from quesadilla.connectors.basic_queues import BaseQueue, BasicQueue
from quesadilla.core.task_executables import Failure, Success
from quesadilla.core.task_metadata import SerializableTask
from quesadilla.core.task_queues import GenericQueuedTask

from quesadilla.runners.workloads.base import BaseWorkload
from quesadilla.runners.workloads.logging import WorkerLoggingExtras


@dataclass(frozen=True)
class Worker(BaseWorkload):
    scheduled_tasks: BasicQueue[SerializableTask[Any]] = field(kw_only=True, repr=False)
    results: BasicQueue[SerializableTask[Any]] = field(kw_only=True, repr=False)

    asyncio_runner: asyncio.Runner = field(default_factory=asyncio.Runner, init=False)

    type: ClassVar[str] = "worker"
    logger: ClassVar[logging.Logger] = logging.getLogger(__name__)

    @cached_property
    def logging_extras(self) -> WorkerLoggingExtras:
        return {
            **super().logging_extras,
            "worker_id": str(self.id),
        }

    def main_loop(self) -> None:
        self.logger.info("Worker starting...", extra=self.logging_extras)

        while not self.stopped.is_set():
            while not self.closed.is_set() and (queued_task := self.next()) is not None:
                self.logger.info(
                    "Processing task %s(%s)",
                    queued_task.task_executable.name,
                    queued_task.id,
                    extra=self.get_task_logging_extras(queued_task),
                )
                executed_task = queued_task.execute(self.asyncio_runner)
                self.result(executed_task)

                match executed_task.wait_for().result:
                    case Success():
                        self.logger.info(
                            "Processed task %s(%s)",
                            queued_task.task_executable.name,
                            queued_task.id,
                            extra=self.get_task_logging_extras(queued_task),
                        )
                    case Failure(exc):  # pragma: nobranch
                        self.logger.error(
                            "Processed task %s(%s) with an exception: %s",
                            queued_task.task_executable.name,
                            queued_task.id,
                            exc,
                            extra=self.get_task_logging_extras(queued_task),
                        )

            time.sleep(0.1)

        self.logger.info("Worker flushing tasks...", extra=self.logging_extras)
        self.flush_outstanding_tasks()

        self.logger.info("Worker exited gracefully", extra=self.logging_extras)

    def flush_outstanding_tasks(self) -> SerializableTask[Any] | None:
        while (queued_task := self.next()) is not None:
            self.results.put(queued_task.serializable)

    def next(self) -> GenericQueuedTask | None:
        try:
            return GenericQueuedTask.from_serializable(
                (task := self.scheduled_tasks.get(timeout=0.1)),
                self.task_queue,
                self.task_queue.get_task_executable(task.task_name),
            )
        except BaseQueue.Empty:
            return None

    def result(self, queued_task: GenericQueuedTask) -> None:
        self.results.put(queued_task.serializable)

    def schedule_for_execution(self, task: GenericQueuedTask) -> None:
        self.scheduled_tasks.put(task.serializable)

    def pull_result(self) -> GenericQueuedTask | None:
        try:
            return GenericQueuedTask.from_serializable(
                (task := self.results.get(timeout=0.1)),
                self.task_queue,
                self.task_queue.get_task_executable(task.task_name),
            )
        except BaseQueue.Empty:
            return None

    def close(self):
        self.logger.info("Worker closing...", extra=self.logging_extras)
        super().close()

    def stop(self):
        self.logger.info("Worker stopping...", extra=self.logging_extras)
        super().stop()
