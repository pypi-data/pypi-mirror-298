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
import time
from dataclasses import dataclass, field
from functools import cached_property
from typing import ClassVar

from quesadilla.core.task_queues import GenericQueuedTask

from quesadilla.runners.workloads.base import BaseWorkload
from quesadilla.runners.workloads.logging import BrokerLoggingExtras
from quesadilla.runners.workloads.worker_selectors import WorkerSelector


@dataclass(frozen=True)
class Broker(BaseWorkload):
    worker_selector: WorkerSelector = field(kw_only=True)

    type: ClassVar[str] = "broker"
    logger: ClassVar[logging.Logger] = logging.getLogger(__name__)

    @cached_property
    def logging_extras(self) -> BrokerLoggingExtras:
        return {
            **super().logging_extras,
            "broker_id": str(self.id),
        }

    def main_loop(self) -> None:
        self.logger.info("Broker starting...", extra=self.logging_extras)

        while not self.stopped.is_set():
            # handling results is more important than scheduling new work
            self.handle_outstanding_tasks()

            if not self.closed.is_set() and (queued_task := self.next()) is not None:
                self.schedule_for_execution(queued_task)
                continue

            time.sleep(0.1)

        self.logger.info(
            "Broker handling outstanding tasks...", extra=self.logging_extras
        )
        self.handle_outstanding_tasks()

        self.logger.info("Broker exited gracefully", extra=self.logging_extras)

    def next(self) -> GenericQueuedTask | None:
        return self.task_queue.pull()

    def schedule_for_execution(self, queued_task: GenericQueuedTask) -> None:
        queued_task = queued_task.start()
        self.task_queue.update(queued_task)
        self.worker_selector.select().schedule_for_execution(queued_task)
        self.logger.info(
            "Scheduled task %s(%s)",
            queued_task.task_executable.name,
            queued_task.id,
            extra=self.get_task_logging_extras(queued_task),
        )

    def handle_outstanding_tasks(self) -> None:
        for worker in self.worker_selector.all():
            while task := worker.pull_result():
                self.result(task)

    def result(self, queued_task: GenericQueuedTask) -> None:
        if queued_task.execution_result.finished:
            queued_task = queued_task.finalize()
        else:
            queued_task = queued_task.reset()

        self.task_queue.update(queued_task)
        self.logger.info(
            "Finalized task %s(%s)",
            queued_task.task_executable.name,
            queued_task.id,
            extra=self.get_task_logging_extras(queued_task),
        )

    def close(self):
        self.logger.info("Broker closing...", extra=self.logging_extras)
        super().close()

    def stop(self):
        self.logger.info("Broker stopping...", extra=self.logging_extras)
        super().stop()
