import pytest
from pyeventic import Event, event

def test_init_defaults():
	event = Event[[], None]()
	assert len(event) == 0
	assert event._func is None # type: ignore # _func is private

def test_event_invalid_callable():
	with pytest.raises(TypeError, match="Expected a callable"):
		event(42) # type: ignore

def test_repr():
	event = Event[[], None]()
	class MyClass:
		clicked = Event[[], None]()
	instance = MyClass()
	
	assert "Event func='None' handlers=0" in repr(event)
	assert "MyClass.clicked" in repr(MyClass.clicked)
	assert "MyClass.clicked" in repr(instance.clicked)

def test_str():
	event = Event[[], None]()
	class MyClass:
		clicked = Event[[], None]()

	assert "Event('MyClass.clicked')" in str(MyClass.clicked)
	assert "Event(None)" in str(event)

def test_len():
	event = Event[[], None]()
	event.subscribe(lambda: None)
	assert len(event) == 1

def test_subscribe_unsubscribe():
	event = Event[[], None]()
	def h(): pass
	
	event.subscribe(h)
	assert h in event._handlers # type: ignore # _handlers is private
	
	event.unsubscribe(h)
	assert h not in event._handlers # type: ignore # _handlers is private

def test_subscribe_duplicate():
	event = Event[[], None]()
	def h(): pass
	
	event.subscribe(h)
	event.subscribe(h) # Duplicate subscription
	assert len(event) == 1

def test_unsubscribe_nonexistent():
	event = Event[[], None]()
	def h(): pass

	# Should not raise
	event.unsubscribe(h)

def test_subscribe_unsubscribe_invalid_callable():
	event = Event[[], None]()
	
	with pytest.raises(TypeError, match="Expected a callable"):
		event.subscribe(42) # type: ignore
	
	with pytest.raises(TypeError, match="Expected a callable"):
		event.unsubscribe(42) # type: ignore

def test_iadd_isub_operators():
	event = Event[[], None]()
	def h(): pass

	event += h
	assert len(event) == 1
	event -= h
	assert len(event) == 0

def test_iadd_isub_invalid_callable():
	event = Event[[], None]()
	
	with pytest.raises(TypeError, match="Expected a callable"):
		event += 42 # type: ignore
	
	with pytest.raises(TypeError, match="Expected a callable"):
		event -= 42 # type: ignore

def test_class_event_decorator():
	class MyClass:
		@event(method=True)
		def my_event(self) -> None: ...
	
	MyClass.my_event() # No self argument required even though the event signature includes it
	assert isinstance(MyClass.my_event, Event)
	assert MyClass.my_event._func.__name__ == "my_event" # type: ignore # _func is private
