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
import random
from collections.abc import Callable, Coroutine
from typing import Any

from quesadilla.connectors.in_memory import ProcessSafeInMemoryConnector
from quesadilla.core import TaskNamespace, async_task, sync_task
from quesadilla.runners import MultiprocessingRunner, RunnerConfig

# configure logging


logger = logging.getLogger(__name__)


# define the task queue


namespace = TaskNamespace("quesadilla", connector=ProcessSafeInMemoryConnector())
queue = namespace.queue("default")


# define some simple tasks


@sync_task(queue)
def simple_sync_task(i: int) -> bool:
    return i == 0


@async_task(queue)
async def simple_async_task(i: int) -> bool:
    return i == 0


@sync_task(queue)
def sometimes_exception_task(i: int) -> bool:
    if random.random() < 0.01:
        raise Exception("(Un)lucky 1%!")
    return i == 0


# helper method for running coroutines in an asyncio runner


def run_coro[**P, T](coro: Callable[P, Coroutine[Any, Any, T]]) -> Callable[P, T]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        return asyncio.run(coro(*args, **kwargs))

    return wrapper


# configure the runner


runner = MultiprocessingRunner(queue, config=RunnerConfig(brokers=2, workers=3))


# we will use this helper function schedule tasks whichever way we can
# to test all possible combinations


def schedule_some_tasks() -> None:
    choices = [
        simple_sync_task.queue,
        simple_async_task.queue,
        sometimes_exception_task.queue,
        run_coro(simple_sync_task.aqueue),
        run_coro(simple_async_task.aqueue),
        run_coro(sometimes_exception_task.aqueue),
    ]
    for _ in range(random.randint(3, 10)):
        random.choice(choices)(random.randint(0, 1))


schedule_some_tasks()
schedule_some_tasks()
schedule_some_tasks()
schedule_some_tasks()
