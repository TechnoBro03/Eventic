import asyncio
import pytest
from typing import Awaitable
from pyeventic import Event

@pytest.mark.asyncio
async def test_invoke_async():
	event = Event[[], Awaitable[None]]()
	results: list[int] = []
	
	async def h1(): results.append(1)
	async def h2(): results.append(2)
	def h3(): results.append(3)
	
	event.subscribe(h1)
	event.subscribe(h2)
	event.subscribe(h3)
	
	# invoke() returns custom _Awaitable
	awaitable = event.invoke()
	assert bool(awaitable) is True
	await awaitable
	
	assert set(results) == {1, 2, 3}

@pytest.mark.asyncio
async def test_invoke_async_exception_ignored():
	event = Event[[], Awaitable[None]]()
	results: list[int] = []

	async def h1(): results.append(1)
	async def h2(): raise ValueError("Handler error")
	def h3(): results.append(3)

	event.subscribe(h1)
	event.subscribe(h2)
	event.subscribe(h3)

	# Without on_error, the exception is ignored and the remaining handlers are still called
	awaitable = event.invoke()
	assert bool(awaitable) is True
	await awaitable

	assert set(results) == {1, 3}

@pytest.mark.asyncio
async def test_call_async():
	event = Event[[], Awaitable[None]]()
	called = False
	
	async def h(): nonlocal called; called = True
	event.subscribe(h)
	
	await event()
	assert called is True

@pytest.mark.asyncio
async def test_fire_and_wait():
	event = Event[[], Awaitable[None]]()
	finish_flag = asyncio.Event()

	async def h():
		await asyncio.sleep(0.1)
		finish_flag.set()

	event.subscribe(h)
	task = event.fire()
	
	assert task in event._tasks # type: ignore # _tasks is private
	await event.wait()
	assert finish_flag.is_set()
	assert len(event._tasks) == 0 # type: ignore # _tasks is private

def test_fire_no_loop_error():
	event = Event[[], Awaitable[None]]()
	
	with pytest.raises(RuntimeError, match="No running event loop"):
		event.fire()

@pytest.mark.asyncio
async def test_on_task_done_cancelled():
	event = Event[[], Awaitable[None]]()
	
	async def slow_handler():
		await asyncio.sleep(1)
		
	event.subscribe(slow_handler)
	task = event.fire()
	
	# Cancel the task immediately
	task.cancel()
	
	try: await task
	except asyncio.CancelledError: ...
	
	# Verify the task was removed from the set
	assert task not in event._tasks # type: ignore # _tasks is private

@pytest.mark.asyncio
async def test_on_task_done_exception():
	event = Event[[], Awaitable[None]]()
	
	async def faulty_handler():
		raise ValueError("Intentional background failure")
		
	event.subscribe(faulty_handler)
	task = event.fire()
	
	# Wait for the task to finish
	await asyncio.gather(task, return_exceptions=True)
	
	# Verify the exception was ignored (not raised) and task was discarded
	assert task.exception() is None
	assert task not in event._tasks # type: ignore # _tasks is private
