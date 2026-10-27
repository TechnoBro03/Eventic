import asyncio
import pytest
from typing import Awaitable
from pyeventic import Event
from pyeventic.awaitable_group import AwaitableGroup

@pytest.mark.asyncio
async def test_awaitable_bool():
	event = Event[[], Awaitable[None]]()
	
	async def h(): pass
	event.subscribe(h)
	
	awaitable = event.invoke()
	assert bool(awaitable) is True
	
	event.unsubscribe(h)
	awaitable = event.invoke()
	assert bool(awaitable) is False

@pytest.mark.asyncio
async def test_awaitable_await():
	event = Event[[], Awaitable[None]]()
	results: list[int] = []
	
	async def h1(): results.append(1)
	async def h2(): results.append(2)
	
	event.subscribe(h1)
	event.subscribe(h2)
	
	awaitable = event.invoke()
	await awaitable
	
	assert set(results) == {1, 2}

@pytest.mark.asyncio
async def test_awaitable_delete_cancels_tasks():
	event = Event[[], Awaitable[None]]()
	task_completed = False
	
	async def h():
		nonlocal task_completed
		await asyncio.sleep(0.2)
		task_completed = True
	
	event.subscribe(h)
	
	awaitable = event.invoke()
	assert bool(awaitable) is True
	
	del awaitable
	await asyncio.sleep(0.3)
	assert not task_completed

@pytest.mark.asyncio
async def test_awaitable_gather():
	event = Event[[], Awaitable[None]]()
	results: list[int] = []
	
	async def h1(): results.append(1)
	async def h2(): results.append(2)
	async def h3(): raise ValueError("Handler error")
	
	event.subscribe(h1)
	event.subscribe(h2)
	event.subscribe(h3)
	
	awaitable = event.invoke()
	await awaitable
	
	assert set(results) == {1, 2}

@pytest.mark.asyncio
async def test_close_handles_coroutine_close_exception():
	ag = AwaitableGroup()

	async def h() -> None:
		try: await asyncio.sleep(.1)
		finally: raise RuntimeError("Cleanup failed")
	
	coro = h()
	coro.send(None) # Start the coroutine

	ag._awaitables.append(coro) # type: ignore # _awaitables is private
	ag.close() # Should not raise
