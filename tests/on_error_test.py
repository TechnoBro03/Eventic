import pytest
from typing import Awaitable, Callable
import inspect
import warnings
from pyeventic import Event

def test_sync_on_error():
	caught: list[Exception] = []
	event = Event[[], None](on_error=caught.append)
	results: list[int] = []

	def h1(): raise ValueError("First")
	def h2(): results.append(2)
	def h3(): raise KeyError("Second")

	event += h1
	event += h2
	event += h3

	event.invoke()
	assert results == [2] # All handlers are called
	assert [type(e) for e in caught] == [ValueError, KeyError]

def test_sync_on_error_raises():
	def on_error(exc: Exception) -> None: raise RuntimeError("on_error failed") from exc
	event = Event[[], None](on_error=on_error)
	results: list[int] = []

	def h1(): raise ValueError("Handler error")
	def h2(): results.append(2)

	event += h1
	event += h2

	with pytest.raises(RuntimeError, match="on_error failed"):
		event.invoke()
	assert results == [] # Handlers after the failing one are not called

def test_hook_exceptions_ignored():
	event = Event[[], None]()
	def hook(e: Event[[], None], h: Callable[[], None | Awaitable[None]]): raise ValueError("Hook error")
	event.on_subscribe += hook

	event += lambda: None
	assert len(event) == 1

@pytest.mark.asyncio
async def test_async_on_error():
	caught: list[Exception] = []
	event = Event[[], Awaitable[None]](on_error=caught.append)
	results: list[int] = []

	def h1(): raise ValueError("Sync")
	async def h2(): results.append(2)
	async def h3(): raise KeyError("Async")

	event += h1
	event += h2
	event += h3

	awaitable = event.invoke()
	assert [type(e) for e in caught] == [ValueError] # Sync handlers are reported during invoke()
	await awaitable
	assert results == [2]
	assert [type(e) for e in caught] == [ValueError, KeyError] # Async handlers once they all finish

@pytest.mark.asyncio
async def test_async_on_error_raises_from_await():
	def on_error(exc: Exception) -> None: raise RuntimeError("on_error failed") from exc
	event = Event[[], Awaitable[None]](on_error=on_error)
	results: list[int] = []

	async def h1(): raise ValueError("Async")
	async def h2(): results.append(2)

	event += h1
	event += h2

	with pytest.raises(RuntimeError, match="on_error failed"):
		await event.invoke()
	assert results == [2] # Already-started async handlers still run to completion

@pytest.mark.asyncio
async def test_async_on_error_raises_closes_pending():
	def on_error(exc: Exception) -> None: raise RuntimeError("on_error failed") from exc
	event = Event[[], Awaitable[None]](on_error=on_error)
	coroutines: list[Awaitable[None]] = []

	async def work(): ...
	def h1():
		coroutines.append(coro := work())
		return coro
	def h2(): raise ValueError("Sync error")

	event += h1
	event += h2

	with warnings.catch_warnings():
		warnings.simplefilter("error") # A "coroutine was never awaited" warning would fail the test
		with pytest.raises(RuntimeError, match="on_error failed"):
			_ = event.invoke()
	# Closed rather than left to raise "coroutine was never awaited" warnings when collected
	assert len(coroutines) == 1
	assert all(inspect.getcoroutinestate(c) == inspect.CORO_CLOSED for c in coroutines) # type: ignore

@pytest.mark.asyncio
async def test_fire_on_error():
	caught: list[Exception] = []
	event = Event[[], Awaitable[None]](on_error=caught.append)
	async def h(): raise ValueError("Background")
	event += h

	event.fire()
	event.fire()
	await event.wait()
	assert [type(e) for e in caught] == [ValueError, ValueError]

@pytest.mark.asyncio
async def test_fire_on_error_raises():
	def on_error(exc: Exception) -> None: raise RuntimeError("on_error failed") from exc
	event = Event[[], Awaitable[None]](on_error=on_error)
	async def h(): raise ValueError("Background")
	event += h

	task = event.fire()
	await event.wait() # Does not raise
	assert isinstance(task.exception(), RuntimeError) # Stored on the task instead
