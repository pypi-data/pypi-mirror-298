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
from abc import ABCMeta
from dataclasses import dataclass, field
from functools import cached_property
from typing import ClassVar

import ulid
from quesadilla.core.task_queues import GenericQueuedTask, TaskQueue

from quesadilla.runners.runners.protocol import Event, Runner
from quesadilla.runners.workloads.logging import ExecutedTaskLoggingExtras
from quesadilla.runners.workloads.protocol import Workload, WorkloadLoggingExtras


@dataclass(frozen=True)
class BaseWorkload(Workload, metaclass=ABCMeta):
    runner: Runner = field(repr=False)
    task_queue: TaskQueue

    id: ulid.ULID = field(default_factory=ulid.ULID, init=False)

    closed: Event = field(kw_only=True, repr=False)
    stopped: Event = field(kw_only=True, repr=False)

    type: ClassVar[str]
    logger: ClassVar[logging.Logger]

    @cached_property
    def logging_extras(self) -> WorkloadLoggingExtras:
        return {
            **self.task_queue.logging_extras,
            **self.runner.logging_extras,
        }

    def get_task_logging_extras(
        self, queued_task: GenericQueuedTask
    ) -> ExecutedTaskLoggingExtras:
        return {
            **queued_task.logging_extras,
            "workload": self.logging_extras,
        }

    def close(self):
        self.closed.set()

    def stop(self):
        self.stopped.set()
