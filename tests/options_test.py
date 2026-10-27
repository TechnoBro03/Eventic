import pytest
from pyeventic import Event, event

def test_event_class_rejects_function():
	def prototype(value: int, /) -> None: ...

	with pytest.raises(TypeError, match=r"Use @event or event\(func\)"):
		Event(prototype) # type: ignore # Event no longer takes a function

	with pytest.raises(TypeError, match=r"Use @event or event\(func\)"):
		@Event # type: ignore # Event no longer takes a function
		def e(value: int, /) -> None: ...

def test_event_function_with_options():
	def prototype(value: int, /) -> None: ...

	e = event(prototype, on_error=print)
	assert e._on_error is print # type: ignore # _on_error is private
	e(1)

def test_invalid_on_error():
	with pytest.raises(TypeError, match="Expected a callable"):
		Event[[], None](on_error="ignore") # type: ignore

def test_event_decorator_function():
	@event
	def e(a: int, /) -> None: ...

	assert isinstance(e, Event)
	assert e._method is False # type: ignore # _method is private
	e(1)

def test_event_decorator_function_with_options():
	@event(on_error=print)
	def e(a: int, /) -> None: ...

	assert isinstance(e, Event)
	assert e._on_error is print # type: ignore # _on_error is private
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

def test_event_decorator_method_validates_self():
	# Without method=True, "self" is validated like any other parameter
	with pytest.raises(TypeError, match="'self' must be positional-only or keyword-only"):
		class MyClass:
			@event
			def e(self, *, a: int) -> None: ...

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

def test_event_decorator_with_options():
	class MyClass:
		@event(method=True, on_error=print)
		def e(self, a: int, /) -> None: ...

	assert MyClass.e._on_error is print # type: ignore # _on_error is private
	MyClass.e(1)

def test_descriptor_copies_options():
	caught: list[Exception] = []

	class MyClass:
		@event(method=True, on_error=caught.append)
		def e(self, a: int, /) -> None: ...

	instance_event = MyClass().e
	assert instance_event._on_error == caught.append # type: ignore # _on_error is private

	def h(a: int): raise ValueError("Handler error")
	instance_event += h
	instance_event(1)
	assert len(caught) == 1 and isinstance(caught[0], ValueError)
