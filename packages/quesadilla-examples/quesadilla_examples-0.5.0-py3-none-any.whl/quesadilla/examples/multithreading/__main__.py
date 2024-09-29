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
import signal
import threading
import time
from types import FrameType

from quesadilla.runners import MultithreadingRunner, RunnerConfig

from quesadilla.examples.multithreading import logger, queue, schedule_some_tasks

if __name__ == "__main__":
    runner = MultithreadingRunner(queue, config=RunnerConfig(brokers=2, workers=3))

    stopped = threading.Event()

    def shutdown(sig: int | None = None, frame: FrameType | None = None) -> None:
        if not stopped.is_set():
            s = signal.Signals(sig) if sig is not None else sig
            if s is not None:
                logger.warning(f"Received signal {s.name}")
            if s in frozenset((signal.SIGTERM, signal.SIGINT)):
                logger.info("Main thread stopping...")
                stopped.set()
                runner.signal(sig)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    logging.basicConfig(
        format="{levelname:7} | {name:36} | {asctime} | {message}",
        style="{",
        level=logging.INFO,
    )

    logger.info("Main thread starting...")

    with runner:

        # run the main loop
        # schedules tasks on the queue indefinitely while the runner is running
        while not stopped.is_set():
            schedule_some_tasks()
            time.sleep(random.random() * 5)

    logger.info("Main thread exited gracefully")
