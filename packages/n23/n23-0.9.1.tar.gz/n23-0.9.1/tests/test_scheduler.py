#
# n23 - data acquisition and processing framework
#
# Copyright (C) 2013-2023 by Artur Wroblewski <wrobell@riseup.net>
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
# ruff: noqa: SLF001

"""
The n23 scheduler unit tests.
"""

import asyncio
import functools
import logging
import time
import typing as tp
from collections import Counter
from collections.abc import AsyncGenerator, AsyncIterator, Awaitable

from n23.fn import concat, identity
from n23.scheduler import Scheduler, TaskHandle, TaskResult, Task, \
    BackgroundTask, logger as s_logger

import pytest
from unittest import mock

logger = logging.getLogger()

@pytest.mark.asyncio
async def test_task_read_awaitable() -> None:
    """
    Test reading data with an awaitable.
    """
    class Reader(Awaitable[str]):
        def __await__(self) -> tp.Generator[None, None, str]:
            yield from ()
            return 'value'

    th = TaskHandle[str]('pressure')
    task = Task(th, 1, Reader(), identity, mock.AsyncMock())

    await task
    assert len(task.queue) == 1
    assert task.queue._data[0].name == 'pressure'
    assert task.queue._data[0].value == 'value'

@pytest.mark.asyncio
async def test_task_read_func() -> None:
    """
    Test reading data with a function.
    """
    async def mock_executor(_: tp.Any, f: tp.Any) -> tp.Any:
        return f()

    reader = lambda: 'value'
    loop = mock.MagicMock()
    loop.run_in_executor = mock_executor

    th = TaskHandle[str]('pressure')
    task = Task(th, 1, reader, identity, mock.AsyncMock())

    await task
    assert task.queue._data[0].name == 'pressure'
    assert task.queue._data[0].value == 'value'

@pytest.mark.asyncio
async def test_task_read_coroutine() -> None:
    """
    Test reading data with a coroutine.
    """
    async def reader() -> str:
        return 'value'

    th = TaskHandle[str]('pressure')
    task = Task(th, 1, reader, identity, mock.AsyncMock())

    await task
    assert task.queue._data[0].name == 'pressure'
    assert task.queue._data[0].value == 'value'

@pytest.mark.timeout(1)
@pytest.mark.asyncio
async def test_coroutine_task_cancel() -> None:
    """
    Test cancellation of a scheduler task running a coroutine.
    """
    async def reader() -> str:
        await asyncio.sleep(0.5)
        return 'value'

    th = TaskHandle[str]('pressure')
    task = Task(th, 1, reader, identity, mock.AsyncMock())
    task.queue = mock.MagicMock()

    try:
        # note: task is cancelled by `wait_for` on timeout
        await asyncio.wait_for(task, timeout=0.1)
    except asyncio.TimeoutError as ex:
        logger.info('ignoring: {}'.format(ex))

    assert not task.queue.put.called

@pytest.mark.timeout(1)
@pytest.mark.asyncio
async def test_async_generator_task_cancel() -> None:
    """
    Test cancellation of a scheduler task running an asynchronous generator.
    """
    async def reader() -> AsyncGenerator[str, None]:
        while True:
            await asyncio.sleep(0.5)
            yield 'value'

    th = TaskHandle[str]('pressure')
    task = Task(th, 1, reader, identity, mock.AsyncMock())
    task.queue = mock.MagicMock()

    try:
        # note: task is cancelled by `wait_for` on timeout
        await asyncio.wait_for(task, timeout=0.1)
    except asyncio.TimeoutError as ex:
        logger.info('ignoring: {}'.format(ex))

    # task has no result
    assert not task.queue.put.called

@pytest.mark.timeout(1)
@pytest.mark.asyncio
async def test_func_task_cancel() -> None:
    """
    Test cancellation of a scheduler task running a function.
    """
    def reader() -> str:
        time.sleep(0.5)
        return 'value'

    th = TaskHandle[str]('pressure')
    task = Task(th, 1, reader, identity, mock.AsyncMock())
    task.queue = mock.MagicMock()

    try:
        await asyncio.wait_for(task, timeout=0.1)
    except asyncio.TimeoutError as ex:
        logger.info('ignoring: {}'.format(ex))

    # task has no result
    assert not task.queue.put.called

@pytest.mark.timeout(1)
@pytest.mark.asyncio
async def test_task_bg_read() -> None:
    """
    Test reading data with background task.
    """
    async def reader() -> AsyncIterator[str]:
        yield 'value'
        yield 'value'
        yield 'value'

    th = TaskHandle[str]('pressure')
    task = BackgroundTask(th, reader, identity, mock.AsyncMock())

    try:
        await task
    except StopAsyncIteration as ex:
        logger.info('ignoring: {}'.format(ex))

    result = task.queue._data
    assert [v.name for v in result] == ['pressure'] * 3
    assert [v.value for v in result] == ['value'] * 3

@pytest.mark.asyncio
async def test_task_read_coroutine_partial() -> None:
    """
    Test reading data with coroutine enclosed with partial.
    """
    async def reader(v: str) -> str:
        return 'value ' + v

    reader = functools.partial(reader, 'test')
    th = TaskHandle[str]('pressure')
    task = Task(th, 1, reader, identity, mock.AsyncMock())

    await task
    assert len(task.queue) == 1
    assert task.queue._data[0].value == 'value test'

def test_scheduler_adding_regular_task() -> None:
    """
    Test adding task with pipeline and sink to scheduler.
    """
    async def source() -> int: return 1
    async def sink(v: TaskResult[int]) -> None: pass

    scheduler = Scheduler()
    handle = scheduler.add(1, 'pressure', source, identity, sink)
    assert not scheduler._bg_tasks
    task = scheduler._tasks[0]
    assert task.handle == handle
    assert task.pipeline == identity
    assert task.sink == sink

def test_scheduler_adding_bg_task() -> None:
    """
    Test adding event-driven task with pipeline and sink to scheduler.
    """
    async def source() -> int: return 1
    async def sink(v: TaskResult[int]) -> None: pass

    scheduler = Scheduler()
    handle = scheduler.add('pressure', source, identity, sink)
    assert not scheduler._tasks
    task = scheduler._bg_tasks[0]
    assert task.handle == handle
    assert task.pipeline == identity
    assert task.sink == sink

@pytest.mark.timeout(5)
@pytest.mark.asyncio
async def test_scheduler_reader_regular() -> None:
    """
    Test scheduler reading data with a coroutine.
    """
    async def reader() -> int:
        return 2

    sink = mock.AsyncMock(side_effect=[None, ValueError('stop')])

    start = time.time()
    scheduler = Scheduler()
    scheduler.add(0.1, 'pressure', reader, identity, sink)
    try:
        await scheduler
    except ValueError as ex:
        logger.warning('ignoring: {}'.format(ex))

    assert scheduler.ctx.tick == 1
    assert scheduler.ctx.time > start

@pytest.mark.asyncio
async def test_scheduler_reader_error() -> None:
    """
    Test scheduler not swallowing error thrown by data reader.
    """
    async def reader() -> tp.NoReturn:
        raise ValueError('test test test')

    sink = mock.AsyncMock()

    scheduler = Scheduler()
    scheduler.add(0.1, 'pressure', reader, identity, sink)
    with pytest.raises(ValueError) as ctx:
        await scheduler

    assert str(ctx.value) == 'test test test'

@pytest.mark.timeout(1)
@pytest.mark.asyncio
async def test_scheduler_reader_timeout() -> None:
    """
    Test scheduler logging warning on data read timeout.
    """
    with mock.patch.object(asyncio, 'wait') as mock_wait:
        task = mock.MagicMock()
        task.get_name.return_value = 'pressure'

        stopper = mock.MagicMock()
        stopper.exception.return_value = ValueError('to be ignored')
        mock_wait.side_effect = [
            [{}, {task}],
            [{stopper}, {}],
        ]

        scheduler = Scheduler()
        scheduler.add(
            0.1, 'pressure', mock.MagicMock(),  identity, mock.MagicMock()
        )
        p_logger = mock.patch.object(s_logger, 'debug')
        with p_logger as f:
            try:
                await scheduler._run_tasks()
            except ValueError as ex:
                logger.warning('ignoring: {}'.format(ex))

            # the timeout was logged and task got cancelled
            f.assert_called_once_with('task pressure timeout')
            task.cancel.assert_called_once_with(
                msg='task cancelled by n23 scheduler due to timeout'
            )

@pytest.mark.timeout(1)
@pytest.mark.asyncio
async def test_scheduler_pipeline_null() -> None:
    """
    Test scheduler skipping sink on pipeline returing null.
    """
    async def reader() -> AsyncIterator[int]:
        yield 1
        yield 1
        raise ValueError('stop reader')

    counter = Counter[int]()
    def pl(v: TaskResult[int]) -> TaskHandle[int] | None:
        counter[v.value] += 1
        return None

    sink = mock.AsyncMock()

    scheduler = Scheduler()
    scheduler.add(0.1, 'pressure', reader, pl, sink)
    assert len(scheduler._tasks) == 1

    with pytest.raises(ValueError) as ctx:
        await scheduler

    assert str(ctx.value) == 'stop reader'
    assert counter[1] == 2
    assert sink.call_count == 0

@pytest.mark.timeout(1)
@pytest.mark.asyncio
async def test_scheduler_sink_error() -> None:
    """
    Test scheduler not swallowing error thrown by sink.
    """
    async def reader() -> int:
        return 1

    sink = mock.AsyncMock()
    sink.side_effect = [ValueError('test test test')]

    scheduler = Scheduler()
    scheduler.add(0.1, 'pressure', reader, identity, sink)
    assert len(scheduler._tasks) == 1

    with pytest.raises(ValueError) as ctx:
        await scheduler

    assert str(ctx.value) == 'test test test'
    sink.assert_called_once()

@pytest.mark.timeout(3)
@pytest.mark.asyncio
async def test_scheduler_cancel() -> None:
    """
    Test cancelling scheduler.
    """
    async def reader() -> int:
        return 1

    async def reader_bg() -> int:
        await asyncio.sleep(0.25)
        return 1

    async def cancel(task: asyncio.Future[None]) -> None:
        await asyncio.sleep(1)
        task.cancel('done')

    sink = mock.AsyncMock()
    sink_bg = mock.AsyncMock()

    scheduler = Scheduler()
    scheduler.add(0.2, 'pressure', reader, identity, sink)
    scheduler.add('gps', reader_bg, identity, sink_bg)

    task = asyncio.ensure_future(scheduler)
    with pytest.raises(asyncio.CancelledError) as ex_ctx:
        await asyncio.gather(cancel(task), task)
    assert str(ex_ctx.value) == 'done'

    # sleep a while and check if all tasks are cancelled
    await asyncio.sleep(1)

    # all scheduler tasks are stopped
    tasks = concat(scheduler._bg_tasks, scheduler._tasks)
    assert all(t._stop for t in tasks)

    # expected 5, but give it a bit of flexibility
    assert 4 <= sink.call_count <= 6

    # expected 4, but give it a bit of flexibility
    assert 3 <= sink_bg.call_count <= 6

    assert len(asyncio.all_tasks()) == 1

@pytest.mark.timeout(3)
@pytest.mark.asyncio
async def test_task_simple() -> None:
    """
    Test simple task execution.
    """
    data = {'result': 0}
    async def flush() -> None:
        data['result'] += 1
        if data['result'] == 3:
            data['done'] = True
            raise ValueError

    scheduler = Scheduler()
    scheduler.call_every(0.1, 'flush', flush)
    try:
        await scheduler
    except ValueError as ex:
        logger.warning('ignoring: {}'.format(ex))

    assert data['done']
    assert data['result'] == 3

# vim: sw=4:et:ai
