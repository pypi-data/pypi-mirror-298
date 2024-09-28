#
# n23 - data acquisition and processing framework
#
# Copyright (C) 2013-2024 by Artur Wroblewski <wrobell@riseup.net>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
N23 scheduler to run asynchronous tasks.
"""

from __future__ import annotations

import abc
import asyncio
import inspect
import logging
import time
import typing as tp
from collections.abc import Awaitable, Coroutine, AsyncGenerator, \
    AsyncIterator, Generator, Iterable
from dataclasses import dataclass
from functools import singledispatchmethod

from .fn import compose, concat, partial
from .timer import Timer
from .queue import NQueue

logger = logging.getLogger(__name__)

T = tp.TypeVar('T')
S = tp.TypeVar('S')

TaskCoroutine: tp.TypeAlias = Coroutine[None, None, T]
SourceFunction: tp.TypeAlias = Awaitable[T] \
    | tp.Callable[
        [],
        T \
        | TaskCoroutine[T] \
        | AsyncGenerator[T, None] \
        | AsyncIterator[T]
]
PipelineFunction: tp.TypeAlias = tp.Callable[['TaskResult[T]'], S | None]
SinkFunction: tp.TypeAlias = tp.Callable[[T], Awaitable[tp.Any]]

@dataclass(frozen=True)
class TaskHandle(tp.Generic[T]):
    """
    Scheduler task handle.
    """
    __slots__ = ('name', )

    name: str

@dataclass(frozen=True)
class TaskResult(tp.Generic[T]):
    """
    Result of task execution.
    """
    __slots__ = ('time', 'name', 'value')

    time: float
    name: str
    value: T

# the protocols below describe the types of the tasks used by the N23
# scheduler; different functionality of the scheduler requires different
# type of a task to execute

class PAnyTask(tp.Protocol):
    """
    Basic N23 scheduler task.

    The task has a task handle and close method.
    """
    handle: TaskHandle[tp.Any]

    def close(self) -> None: ...

class PRegularTask(PAnyTask):
    """
    N23 scheduler task executed at regular time intervals.
    """
    interval: float

class PDataTask(PAnyTask):
    """
    N23 scheduler task with data buffering, pipeline function, and sink to
    process the data.
    """
    queue: NQueue[tp.Any]
    pipeline: PipelineFunction[tp.Any, tp.Any]
    sink: SinkFunction[tp.Any]

@dataclass(frozen=False)
class Context:
    """
    N23 scheduler context.
    """
    __slots__ = ('tick', 'time', 'on_tick')

    # timer cycle tick
    tick: int

    # time at the start of timer cycle
    time: float

    # event triggered when all tasks completed in given timer cycle
    on_tick: asyncio.Event

class Scheduler(Awaitable[None]):
    """
    N23 scheduler to execute asynchronous tasks.

    :var ctx: Scheduler context.
    :var timeout: Asynchronous task timeout.
    """
    def __init__(self, *, timeout: tp.Optional[float]=None):
        self.timeout = timeout

        self._tasks: list[Task[tp.Any, tp.Any]] = []
        self._bg_tasks: list[BackgroundTask[tp.Any, tp.Any]] = []
        self._s_tasks: list[SimpleTask] = []

        self.ctx = Context(-1, time.time(), asyncio.Event())

    @singledispatchmethod
    def add(  # noqa: PLR0913
            self,
            interval: float,
            name: str,
            source: SourceFunction[T],
            pipeline: PipelineFunction[T, S],
            sink: SinkFunction[S],
            *,
            max_len: int=1000,
    ) -> TaskHandle[T]:
        """
        Add an asynchronous task to the scheduler.

        Two forms of the method are supported::

            add(interval, name, source, pipeline, sink)
            add(name, source, pipeline, sink)

        Tasks are executed at regular intervals (first form) or on the
        event-driven basis in the background (second form).

        Data from `source` is buffered in a queue. Pipeline and sink are
        executed whenever there is data in the buffer.

        Pipeline and sink receive object of class :py:class:`n23.TaskResult`
        as its first parameter. Use `functools.partial` to set default
        parameters if the functions have more parameters.

        If `interval` is specified, then asynchronous task is run at
        regular intervals with a timer, thus obtaining equally spaced time
        series. Otherwise, task is run in background and unevenly spaced
        time series of data is generated.

        :param interval: Run task at regular time intervals if specified.
        :param name: Name (identifier) of the task.
        :param source: Coroutine or function to source data.
        :param pipeline: Function to process source data.
        :param sink: Coroutine to store or forward data.

        .. seealso::

           - :py:class:`n23.TaskResult`
        """
        raise NotImplementedError(
            'Method not implemented for type: {}'.format(type(name))
        )

    @add.register(float)
    @add.register(int)
    def _add_even(  # noqa: PLR0913
            self,
            interval: float,
            name: str,
            source: SourceFunction[T],
            pipeline: PipelineFunction[T, S],
            sink: SinkFunction[S],
            *,
            max_len: int=1000,
    ) -> TaskHandle[T]:
        """
        Add task to be run at regular time intervals.
        """
        handle = TaskHandle[T](name)
        task = Task(handle, interval, source, pipeline, sink, max_len=max_len)
        self._tasks.append(task)
        return handle

    @add.register(str)
    def _add_uneven(
            self,
            name: str,
            source: SourceFunction[T],
            pipeline: PipelineFunction[T, S],
            sink: SinkFunction[S],
            *,
            max_len: int=1000,
    ) -> TaskHandle[T]:
        """
        Add task to be run in background.
        """
        handle = TaskHandle[T](name)
        task = BackgroundTask(handle, source, pipeline, sink, max_len=max_len)
        self._bg_tasks.append(task)
        return handle

    def call_every(
            self,
            interval: float,
            name: str,
            source: SourceFunction[tp.Any],
    ) -> TaskHandle[tp.Any]:
        """
        Submit task to the scheduler and execute it at regular intervals.

        :param interval: Run task at regular time intervals if specified.
        :param name: Name (identifier) of the task.
        :param source: Coroutine or function to execute as a task.
        """
        handle = TaskHandle[tp.Any](name)
        task = SimpleTask(handle, interval, source)
        self._s_tasks.append(task)
        return handle

    def __await__(self) -> Generator[tp.Any, None, None]:
        """
        Start scheduler.
        """
        # always run the regular tasks loop, even if there are no tasks, so
        # the scheduler tick is generated
        reg_task = asyncio.ensure_future(self._run_tasks())
        tasks: list[Awaitable[None]] = [reg_task]

        # add background tasks
        tasks.extend(t for t in self._bg_tasks)

        # add pipeline and sink executors
        items = concat(self._tasks, self._bg_tasks)
        process = self._process_data
        tasks.extend(process(t.queue, t.pipeline, t.sink) for t in items)
        try:
            yield from asyncio.gather(*tasks).__await__()
        finally:
            # close all tasks
            to_close: Iterable[PAnyTask] = concat(
                self._bg_tasks,
                self._tasks,
                self._s_tasks,
            )
            for t in to_close:
                t.close()
            reg_task.cancel(msg='n23 scheduler stopping')

    async def _process_data(
            self,
            queue: NQueue[TaskResult[T]],
            pipeline: PipelineFunction[T, S],
            sink: SinkFunction[S],
    ) -> None:
        while True:
            value = await queue.get()
            if (result := pipeline(value)) is not None:
                await sink(result)

    async def _run_tasks(self) -> None:
        tasks: list[PRegularTask] = list(concat(self._tasks, self._s_tasks))  # type: ignore
        intervals = set(t.interval for t in tasks)
        if len(intervals) > 1:
            # TODO: add support for multiplies of the main interval
            raise ValueError('Single interval is supported only')
        elif not intervals:
            interval = 1.0
        else:
            interval = intervals.pop()
        assert not intervals

        timer = Timer(interval)
        timeout = interval * 0.25 if self.timeout is None else self.timeout

        ctx = self.ctx
        on_tick = ctx.on_tick
        wait_tasks = partial(
            asyncio.wait,
            timeout=timeout,
            return_when=asyncio.FIRST_EXCEPTION
        )
        create_task: tp.Callable[[tp.Any], tp.Any] = asyncio.ensure_future
        try:
            timer.start()
            while True:
                await timer

                ctx.time = time.time()
                ctx.tick = timer._tick  # noqa: SLF001

                if tasks:
                    # start tasks; after timeout, the pending tasks are
                    # cancelled
                    current_tasks = [create_task(t) for t in tasks]
                    done, pending = await wait_tasks(current_tasks)

                    # crash software on error
                    error = next((e for t in done if (e := t.exception())), None)
                    if error:
                        raise error

                    for t in pending:
                        if __debug__:
                            logger.debug('task {} timeout'.format(
                                t.get_name()
                            ))

                        # try to cancel task to make it available again
                        t.cancel(msg='task cancelled by n23 scheduler due to timeout')

                on_tick.set()
                on_tick.clear()
        finally:
            timer.close()

#
# implementation of various tasks executed by the N23 scheduler; see also
# tasks protocols defined above
#

class TaskBase(tp.Generic[T], Awaitable[None]):
    """
    Abstract class for N23 scheduler task.

    :var handle: Scheduler task handle.
    :var source: Coroutine or function to read source data.

    :var _runner: Callable to create asynchronous task for the source
        function.
    :var _stop: Task is about to terminate if true.
    """
    _runner: tp.Callable[[], TaskCoroutine[T]]

    def __init__(
            self,
            handle: TaskHandle[T],
            source: SourceFunction[T],
    ):
        """
        Create task executor.
        """
        self.handle = handle
        self.source = source
        self._stop = False

        create_task: tp.Callable[[tp.Any], TaskCoroutine[T]] \
                = asyncio.ensure_future

        if inspect.isawaitable(source):
            self._runner = lambda: create_task(source)
            logger.info('{} is awaitable'.format(source))
        elif inspect.iscoroutinefunction(source):
            self._runner = compose(source, create_task)  # type: ignore
            logger.info('{} is coroutine function'.format(source))
        elif inspect.isasyncgenfunction(source):
            self._runner = compose(source().__anext__, create_task)  # type: ignore
            logger.info('{} is asynchronous generator'.format(source))
        else:
            loop = asyncio.get_event_loop()
            self._runner = partial(loop.run_in_executor, None, source)  # type: ignore[assignment]
            logger.info('{} is function, will be run in executor' .format(source))

    @abc.abstractmethod
    def __await__(self) -> Generator[None, None, None]:
        ...

    def close(self) -> None:
        """
        Request closing of the task.
        """
        self._stop = True

class SimpleTask(TaskBase[tp.Any]):
    """
    Simple task reading data without data processing.

    :var interval: Time interval at which the task is executed.

    .. seealso:: :py:meth:`.Scheduler.call_every`
    """
    def __init__(
            self,
            handle: TaskHandle[T],
            interval: float,
            source: SourceFunction[tp.Any],
    ):
        super().__init__(handle, source)
        self.interval = interval

    def __await__(self) -> Generator[None, None, None]:
        """
        Execute task.
        """
        try:
            yield from self._runner().__await__()
        except asyncio.CancelledError:
            if __debug__:
                logger.debug('task {} is cancelled, stopped={}'.format(
                    self.handle.name, self._stop
                ))
            if self._stop:
                raise

class DataTask(tp.Generic[T, S], TaskBase[T]):
    """
    Abstract class for a scheduler task processing data from source.

    :var handle: Scheduler task handle.
    :var source: Coroutine or function to source data.
    :var pipeline: Function to process source data.
    :var sink: Coroutine to store or forward data.
    :var queue: Buffer containing unprocessed data.
    :var max_len: Length of buffer for unprocessed data.

    .. seealso:: :py:meth:`.Scheduler.add`
    """
    def __init__(
            self,
            handle: TaskHandle[T],
            source: SourceFunction[T],
            pipeline: PipelineFunction[T, S],
            sink: SinkFunction[S],
            *,
            max_len: int=1000,
    ):
        super().__init__(handle, source)
        self.pipeline = pipeline
        self.sink = sink
        self.queue = NQueue[TaskResult[T]](max_size=max_len)
        self.max_len = max_len

    async def _execute_task(self, task: Coroutine[None, None, T]) -> None:
        """
        Execute task and put result of the task into the buffer queue.

        If task execution is cancelled, then the cancellation error is
        ignored.
        """
        try:
            result = await task
        except asyncio.CancelledError:
            if __debug__:
                logger.debug('task {} is cancelled, stopped={}'.format(
                    self.handle.name, self._stop
                ))
            if self._stop:
                raise
        else:
            tr = TaskResult(time.time(), self.handle.name, result)

            if __debug__ and self.queue.full():
                logger.debug(
                    'queue for {} is about to drop task results'
                    .format(self.handle.name)
                )
            self.queue.put(tr)

class Task(DataTask[T, S]):
    """
    N23 scheduler task procecssing data at regular intervals.

    :var interval: Time interval at which the task is executed.

    .. seealso:: :py:meth:`.Scheduler.add`
    """
    def __init__(  # noqa: PLR0913
            self,
            handle: TaskHandle[T],
            interval: float,
            source: SourceFunction[T],
            pipeline: PipelineFunction[T, S],
            sink: SinkFunction[S],
            *,
            max_len: int=1000,
    ):
        super().__init__(handle, source, pipeline, sink)
        self.interval = interval

    def __await__(self) -> Generator[None, None, None]:
        """
        Execute task.
        """
        yield from self._execute_task(self._runner()).__await__()

class BackgroundTask(DataTask[T, S]):
    """
    N23 scheduler task processing data in background.
    """
    def __await__(self) -> Generator[None, None, None]:
        """
        Execute task.
        """
        while not self._stop:
            yield from self._execute_task(self._runner()).__await__()

__all__ = ['Scheduler', 'TaskResult', 'TaskHandle']

# vim: sw=4:et:ai
