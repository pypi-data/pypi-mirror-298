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
import random

from quesadilla.connectors.in_memory import ThreadSafeInMemoryConnector
from quesadilla.core import Failure, Success, TaskNamespace, sync_task
from quesadilla.runners import MultithreadingRunner, RunnerConfig

namespace = TaskNamespace("quesadilla", connector=ThreadSafeInMemoryConnector())
queue = namespace.queue("default")


@sync_task(queue)
def simple_task(i: int) -> bool:
    return i == 0


@sync_task(queue)
def exception_task() -> bool:
    raise RuntimeError("oi")


if __name__ == "__main__":
    # simulate someone adding jobs to the queue
    tasks = [simple_task.queue(random.choice((0, 1))) for _ in range(20)]
    tasks.extend([exception_task.queue() for _ in range(2)])

    runner = MultithreadingRunner(queue, config=RunnerConfig(brokers=2, workers=5))

    logging.basicConfig(
        format="{levelname:7} | {name:36} | {asctime} | {message}",
        style="{",
        level=logging.INFO,
    )

    with runner:
        for task in tasks:
            match task.wait_for().result:
                case Success(res):
                    logging.info(f"Task finished with result: {res}")
                case Failure(exc):
                    logging.error(f"Task finished with exception: {exc}")
