import pytest
from pyeventic import Event

def test_once_decorator():
	event = Event[[], None]()
	count = 0
	def h(): nonlocal count; count += 1
	
	event.once(h)
	event.invoke()
	event.invoke()
	
	assert count == 1
	assert len(event) == 0

def test_once_remove_before_invoke():
	event = Event[[], None]()
	called = False
	def h(): nonlocal called; called = True
	
	once_handler = event.once(h)
	event.unsubscribe(once_handler)
	
	event.invoke()
	assert not called
	assert len(event) == 0

def test_once_invalid_callable():
	event = Event[[], None]()
	
	with pytest.raises(TypeError, match="Expected a callable"):
		event.once(42) # type: ignore
