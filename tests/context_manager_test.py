import pytest
from typing import Awaitable
from pyeventic import Event

def test_sync_context_manager():
	event = Event[[], None]()
	def h(): pass
	
	with event.subscribed(h):
		assert len(event) == 1
	assert len(event) == 0

@pytest.mark.asyncio
async def test_async_context_manager():
	event = Event[[], Awaitable[None]]()
	def h(): pass
	
	async with event.subscribed(h):
		assert len(event) == 1
	assert len(event) == 0

def test_context_manager_invalid_callable():
	event = Event[[], None]()
	
	with pytest.raises(TypeError, match="Expected a callable"):
		with event.subscribed(42): # type: ignore
			pass
