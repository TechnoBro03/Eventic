import asyncio
import pytest
from typing import Awaitable, Callable
import inspect
from pyeventic import Event, event
from pyeventic.awaitable_group import AwaitableGroup

### Basic Functional Tests ###

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

### Descriptor Tests ###

class Owner:
	evt = Event[[], None]()

def test_descriptor_instance_creation():
	o1 = Owner()
	o2 = Owner()
	# Accessing from instances should create separate Event objects
	assert o1.evt is not o2.evt
	assert o1.evt is not Owner.evt
	assert o1.evt._owner is Owner # type: ignore # _owner is private
	assert o1.evt._name == "evt" # type: ignore # _name is private

def test_descriptor_set_prevention():
	o = Owner()
	original_evt = o.evt
	o.evt = Event[[], None]() # Should be ignored by __set__
	assert o.evt is original_evt

### on_subscribe / on_unsubscribe ###

def test_subscription_events():
	event = Event[[], None]()
	sub_log: list[Callable[[], None | Awaitable[None]]] = []
	unsub_log: list[Callable[[], None | Awaitable[None]]] = []
	
	event.on_subscribe.subscribe(lambda e, h: sub_log.append(h))
	event.on_unsubscribe.subscribe(lambda e, h: unsub_log.append(h))
	
	def h(): pass
	event.subscribe(h)
	event.unsubscribe(h)
	
	assert sub_log == [h]
	assert unsub_log == [h]

def test_subscription_readonly():
	event = Event[[], None]()
	sub = event.on_subscribe
	unsub = event.on_unsubscribe
	
	event.on_subscribe = Event()
	event.on_unsubscribe = Event()

	assert event.on_subscribe is sub
	assert event.on_unsubscribe is unsub

### Sync Tests ###

def test_invoke_sync():
	event = Event[[], None]()
	results: list[int] = []
	
	def h1(): results.append(1)
	def h2(): results.append(2)
	
	event.subscribe(h1)
	event.subscribe(h2)
	
	# invoke() custom _Awaitable (empty for sync handlers)
	event.invoke()
	assert set(results) == {1, 2}

def test_invoke_exception_swallowing():
	event = Event[[], None]()
	results: list[int] = []
	
	def h1(): results.append(1)
	def h2(): raise ValueError("Handler error")
	def h3(): results.append(3)
	
	event.subscribe(h1)
	event.subscribe(h2)
	event.subscribe(h3)
	
	# invoke() should swallow exceptions
	event.invoke()
	assert set(results) == {1, 3}

def test_call_sync():
	event = Event[[], None]()
	called = False
	
	def h(): nonlocal called; called = True
	event.subscribe(h)
	
	event()
	assert called is True

### Async Tests ###

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
async def test_invoke_async_exception_swallowing():
	event = Event[[], Awaitable[None]]()
	results: list[int] = []
	
	async def h1(): results.append(1)
	async def h2(): raise ValueError("Handler error")
	def h3(): results.append(3)
	
	event.subscribe(h1)
	event.subscribe(h2)
	event.subscribe(h3)
	
	# invoke() should swallow exceptions
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
	
	# Verify the exception was swallowed and task was discarded
	assert task not in event._tasks # type: ignore # _tasks is private

### Once ###

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

### Context Manager Tests ###

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

### AwaitableGroup Tests ###

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


### Ordering Tests ###

def test_invoke_subscription_order():
	event = Event[[], None]()
	results: list[int] = []

	for i in range(10):
		event.subscribe(lambda i=i: results.append(i)) # type: ignore # Default arg captures the loop value

	event.invoke()
	assert results == list(range(10))

def test_resubscribe_moves_to_end():
	event = Event[[], None]()
	results: list[int] = []
	def h1(): results.append(1)
	def h2(): results.append(2)

	event += h1
	event += h2
	event -= h1
	event += h1

	event.invoke()
	assert results == [2, 1]

### Introspection Tests ###

def test_update_wrapper():
	def on_change(value: int, /) -> None:
		"""Docstring of the prototype."""

	e = event(on_change)
	assert e.__name__ == "on_change" # type: ignore # Set by update_wrapper
	assert e.__doc__ == "Docstring of the prototype."
	assert e.__wrapped__ is on_change # type: ignore # Set by update_wrapper
	assert str(inspect.signature(e)) == "(value: int, /) -> None"

def test_update_wrapper_per_instance():
	class MyClass:
		@event(method=True)
		def changed(self, value: int, /) -> None:
			"""Docstring of the method prototype."""

	assert MyClass().changed.__doc__ == "Docstring of the method prototype."

def test_descriptor_instance_cached():
	o = Owner()
	assert o.evt is o.evt

### Options Tests ###

def test_event_class_rejects_function():
	def prototype(value: int, /) -> None: ...

	with pytest.raises(TypeError, match=r"Use @event or event\(func\)"):
		Event(prototype) # type: ignore # Event no longer takes a function

	with pytest.raises(TypeError, match=r"Use @event or event\(func\)"):
		@Event # type: ignore # Event no longer takes a function
		def e(value: int, /) -> None: ...

def test_event_decorator_function():
	@event
	def e(a: int, /) -> None: ...

	assert isinstance(e, Event)
	assert e._method is False # type: ignore # _method is private
	e(1)

def test_event_decorator_staticmethod_in_class():
	class MyClass:
		@event
		@staticmethod
		def e(a: int, /) -> None: ...

	MyClass.e(1)

def test_event_decorator_method_keeps_self():
	class MyClass:
		# Without method=True, "self" is part of the event signature
		@event
		def e(self, a: int, /) -> None: ...

	received: list[tuple[MyClass, int]] = []
	instance = MyClass()
	MyClass.e += lambda obj, a: received.append((obj, a))
	MyClass.e(instance, 1)
	assert received == [(instance, 1)]

def test_keyword_parameter_named_self():
	# Event's own methods take "self" positionally, so an event parameter can also be named "self"
	@event
	def e(*, self: int) -> None: ...

	received: list[int] = []
	e += lambda self: received.append(self)
	e(self=1)
	e.invoke(self=2)
	assert received == [1, 2]

@pytest.mark.asyncio
async def test_keyword_parameter_named_self_fire():
	@event
	async def e(*, self: int) -> None: ...

	received: list[int] = []
	async def handler(*, self: int) -> None: received.append(self)
	e += handler
	await e.fire(self=1)
	assert received == [1]

def test_event_manual_class_attribute():
	class MyClass:
		e = Event[[int], None]()

	MyClass.e(1)
