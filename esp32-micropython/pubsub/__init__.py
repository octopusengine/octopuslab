# The MIT License (MIT)
# Copyright (c) 2020 Jan Cespivo

__version__ = "1.0.0"

from collections import deque
from sys import print_exception
from _thread import allocate_lock, start_new_thread


# import pyb


class Semaphore:
    def __init__(self):
        self._counter = 0
        self._lock = allocate_lock()
        self._lock.acquire()
        self._exception = None

    def acquire(self) -> bool:
        # pyb.disable_irq()
        if self._counter == 0:
            # pyb.enable_irq()
            self._lock.acquire()
            if self._exception:
                exception, self._exception = self._exception, None
                raise exception
            # pyb.disable_irq()

        self._counter -= 1

        if self._counter == 0:
            self._lock.acquire(False)

        # pyb.enable_irq()
        return True

    def release(self) -> None:
        # pyb.disable_irq()
        self._counter += 1
        if self._counter == 1 and self._lock.locked():
            self._lock.release()
        # pyb.enable_irq()

    def exception(self, exception) -> None:
        self._exception = exception
        self._lock.release()


class PubSub:
    def __init__(self, maxlen: int) -> None:
        self._started = False
        self._semaphore = Semaphore()
        self._queue = deque(tuple(), maxlen)
        self._subscribers = {}

    def publish(self, name, *args, **kwargs) -> None:
        if name not in self._subscribers:
            return
        # TODO this line is adept to pyb.disable_irq() but deque.append should be atomic
        self._queue.append((name, args, kwargs))
        self._semaphore.release()

    def subscribe(self, name, subscriber) -> None:
        # TODO adept to pyb.disable_irq()
        try:
            self._subscribers[name].append(subscriber)
        except KeyError:
            self._subscribers[name] = [subscriber]

    def _run(self) -> None:
        while self._semaphore.acquire():
            name, args, kwargs = self._queue.popleft()
            for subscriber in self._subscribers[name]:
                try:
                    subscriber(*args, **kwargs)
                except Exception as exc:
                    print_exception(exc)

    def start(self) -> None:
        if self._started:
            # TODO (it might be idempotent) so return
            raise RuntimeError('Pubsub is already started')
        self._started = True
        start_new_thread(self._run, ())

    def stop(self) -> None:
        if not self._started:
            # TODO (it might be idempotent) so return
            raise RuntimeError('Pubsub is already stopped')
        self._started = False
        self._semaphore.exception(SystemExit)
