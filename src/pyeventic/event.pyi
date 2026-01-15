import asyncio
from typing import Any, AsyncContextManager, Awaitable, Callable, Coroutine, Concatenate, ContextManager, Generic, ParamSpec, TypeVar, overload

P = ParamSpec("P")
"""The signature of an Event."""

R = TypeVar("R", None, Awaitable[None])
"""Return type for an Event. `None` for synchronous Events or `Awaitable[None]` for asynchronous Events."""

class Event(Generic[P, R]):
	"""
	A thread-safe, strongly typed event.

	Supports both synchronous and asynchronous events, decorators, one-time handlers, and context-managed subscriptions.

	See `Eventic Documentation <https://github.com/TechnoBro03/Eventic/>`_ for more information.
	"""

	def __init__(self, func: Callable[P, R] | None = None) -> None:
		"""
		Initialize a new Event.

		:param func: An optional function to define the signature of the event.
		:type func: Callable[P, R] | None
		:raises TypeError: If func is not Callable or None.
		"""
	
	def __repr__(self) -> str:
		"""
		Return a detailed string representation of this Event.

		Includes the bound function name (if any), owner class and attribute name (if any), and number of subscribed
		handlers and background tasks.

		:return: The detailed string representation of this Event.
		:rtype: str
		"""

	def __str__(self) -> str:
		"""
		Return a user-friendly string representation of this Event.

		:return: The user-friendly string representation of this Event.
		:rtype: str
		"""

	def __len__(self) -> int:
		"""
		Return the number of handlers subscribed to this event.

		:return: The number of subscribed handlers.
		:rtype: int
		"""

	@overload
	def subscribe(self: "Event[P, None]", handler: Callable[P, None]) -> Callable[P, None]:
		"""
		Subscribe a handler to this event.

		| The handler is invoked whenever the event is fired and order of invocation is not guaranteed.
		| A handler may only be subscribed once; subsequent subscriptions of the same handler have no effect.

		:param handler: The handler to subscribe.
		:type handler: Callable[P, None]
		:return: The original callable.
		:rtype: Callable[P, None]
		:raises TypeError: If handler is not Callable.
		"""

	@overload
	def subscribe(self: "Event[P, Awaitable[None]]", handler: Callable[P, None]) -> Callable[P, None]:
		"""
		Subscribe a handler to this event.

		| The handler is invoked whenever the event is fired and order of invocation is not guaranteed.
		| A handler may only be subscribed once; subsequent subscriptions of the same handler have no effect.

		:param handler: The handler to subscribe.
		:type handler: Callable[P, None]
		:return: The original callable.
		:rtype: Callable[P, None]
		:raises TypeError: If handler is not Callable.
		"""

	@overload
	def subscribe(self: "Event[P, Awaitable[None]]", handler: Callable[P, Awaitable[None]]) -> Callable[P, Awaitable[None]]:
		"""
		Subscribe a handler to this event.

		| The handler is invoked whenever the event is fired and order of invocation is not guaranteed.
		| A handler may only be subscribed once; subsequent subscriptions of the same handler have no effect.

		:param handler: The handler to subscribe.
		:type handler: Callable[P, Awaitable[None]]
		:return: The original callable.
		:rtype: Callable[P, Awaitable[None]]
		:raises TypeError: If handler is not Callable.
		"""
	
	@overload
	def unsubscribe(self: "Event[P, None]", handler: Callable[P, None]) -> None:
		"""
		Unsubscribe a handler from this event.

		If the handler is not currently subscribed, this method does nothing.

		:param handler: The handler to unsubscribe.
		:type handler: Callable[P, None]
		:raises TypeError: If handler is not Callable.
		"""

	@overload
	def unsubscribe(self: "Event[P, Awaitable[None]]", handler: Callable[P, None]) -> None:
		"""
		Unsubscribe a handler from this event.

		If the handler is not currently subscribed, this method does nothing.

		:param handler: The handler to unsubscribe.
		:type handler: Callable[P, None]
		:raises TypeError: If handler is not Callable.
		"""

	@overload
	def unsubscribe(self: "Event[P, Awaitable[None]]", handler: Callable[P, Awaitable[None]]) -> None:
		"""
		Unsubscribe a handler from this event.

		If the handler is not currently subscribed, this method does nothing.

		:param handler: The handler to unsubscribe.
		:type handler: Callable[P, Awaitable[None]]
		:raises TypeError: If handler is not Callable.
		"""

	@overload
	def invoke(self: "Event[P, Awaitable[None]]", *args: P.args, **kwargs: P.kwargs) -> Coroutine[Any, Any, None]: ...
	# Docstring left blank to allow inheritance from function

	@overload
	def invoke(self: "Event[P, None]", *args: P.args, **kwargs: P.kwargs) -> None: ...
	# Docstring left blank to allow inheritance from function

	def fire(self: "Event[P, Awaitable[None]]", *args: P.args, **kwargs: P.kwargs) -> asyncio.Task[None]: ...
	# Docstring left blank to allow inheritance from function

	def wait(self: "Event[P, Awaitable[None]]") -> Coroutine[Any, Any, None]:
		"""Wait for all currently running event invocations to complete."""
	
	@overload
	def once(self: "Event[P, None]", handler: Callable[P, None]) -> Callable[P, None]:
		"""
		Subscribe a handler to this event that will be invoked only once.

		To unsubscribe the handler before it is invoked, unsubscribe the **returned wrapper**.

		:param handler: The handler to subscribe.
		:type handler: Callable[P, None]
		:return: The wrapped callable.
		:rtype: Callable[P, None]
		:raises TypeError: If handler is not Callable.
		"""

	@overload
	def once(self: "Event[P, Awaitable[None]]", handler: Callable[P, None]) -> Callable[P, None]:
		"""
		Subscribe a handler to this event that will be invoked only once.

		To unsubscribe the handler before it is invoked, unsubscribe the **returned wrapper**.

		:param handler: The handler to subscribe.
		:type handler: Callable[P, None]
		:return: The wrapped callable.
		:rtype: Callable[P, None]
		:raises TypeError: If handler is not Callable.
		"""

	@overload
	def once(self: "Event[P, Awaitable[None]]", handler: Callable[P, Awaitable[None]]) -> Callable[P, Awaitable[None]]:
		"""
		Subscribe a handler to this event that will be invoked only once.

		To unsubscribe the handler before it is invoked, unsubscribe the **returned wrapper**.

		:param handler: The handler to subscribe.
		:type handler: Callable[P, Awaitable[None]]
		:return: The wrapped callable.
		:rtype: Callable[P, Awaitable[None]]
		:raises TypeError: If handler is not Callable.
		"""
	
	@overload
	def subscribed(self: "Event[P, None]", handler: Callable[P, None]) -> ContextManager["Event[P, None]"]:
		"""
		Get a context manager that subscribes a handler to this event upon entering the context
		and unsubscribes it upon exiting.

		:param handler: The handler to subscribe.
		:type handler: Callable[P, None]
		:return: A context manager for the subscription.
		:rtype: ContextManager[Event[P, None]]
		:raises TypeError: If handler is not Callable.
		"""

	@overload
	def subscribed(self: "Event[P, Awaitable[None]]", handler: Callable[P, None]) -> AsyncContextManager["Event[P, Awaitable[None]]"]:
		"""
		Get a context manager that subscribes a handler to this event upon entering the context
		and unsubscribes it upon exiting.

		:param handler: The handler to subscribe.
		:type handler: Callable[P, None]
		:return: A context manager for the subscription.
		:rtype: AsyncContextManager[Event[P, Awaitable[None]]]
		:raises TypeError: If handler is not Callable.
		"""

	@overload
	def subscribed(self: "Event[P, Awaitable[None]]", handler: Callable[P, Awaitable[None]]) -> AsyncContextManager["Event[P, Awaitable[None]]"]:
		"""
		Get a context manager that subscribes a handler to this event upon entering the context
		and unsubscribes it upon exiting.

		:param handler: The handler to subscribe.
		:type handler: Callable[P, Awaitable[None]]
		:return: A context manager for the subscription.
		:rtype: AsyncContextManager[Event[P, Awaitable[None]]]
		:raises TypeError: If handler is not Callable.
		"""

	@overload
	def __iadd__(self: "Event[P, None]", handler: Callable[P, None]) -> "Event[P, R]":
		"""
		Subscribe a handler to this event.

		| The handler is invoked whenever the event is fired and order of invocation is not guaranteed.
		| A handler may only be subscribed once; subsequent subscriptions of the same handler have no effect.

		:param handler: The handler to subscribe.
		:type handler: Callable[P, None]
		:return: The event instance.
		:rtype: Event[P, None]
		:raises TypeError: If handler is not Callable.
		"""

	@overload
	def __iadd__(self: "Event[P, Awaitable[None]]", handler: Callable[P, None]) -> "Event[P, R]":
		"""
		Subscribe a handler to this event.

		| The handler is invoked whenever the event is fired and order of invocation is not guaranteed.
		| A handler may only be subscribed once; subsequent subscriptions of the same handler have no effect.

		:param handler: The handler to subscribe.
		:type handler: Callable[P, None]
		:return: The event instance.
		:rtype: Event[P, Awaitable[None]]
		:raises TypeError: If handler is not Callable.
		"""

	@overload
	def __iadd__(self: "Event[P, Awaitable[None]]", handler: Callable[P, Awaitable[None]]) -> "Event[P, R]":
		"""
		Subscribe a handler to this event.

		| The handler is invoked whenever the event is fired and order of invocation is not guaranteed.
		| A handler may only be subscribed once; subsequent subscriptions of the same handler have no effect.

		:param handler: The handler to subscribe.
		:type handler: Callable[P, Awaitable[None]]
		:return: The event instance.
		:rtype: Event[P, Awaitable[None]]
		:raises TypeError: If handler is not Callable.
		"""

	@overload
	def __isub__(self: "Event[P, None]", handler: Callable[P, None]) -> "Event[P, R]":
		"""
		Unsubscribe a handler from this event.

		:param handler: The handler to unsubscribe.
		:type handler: Callable[P, None]
		:return: The event instance.
		:rtype: Event[P, None]
		"""

	@overload
	def __isub__(self: "Event[P, Awaitable[None]]", handler: Callable[P, None]) -> "Event[P, R]":
		"""
		Unsubscribe a handler from this event.

		:param handler: The handler to unsubscribe.
		:type handler: Callable[P, None]
		:return: The event instance.
		:rtype: Event[P, Awaitable[None]]
		"""

	@overload
	def __isub__(self: "Event[P, Awaitable[None]]", handler: Callable[P, Awaitable[None]]) -> "Event[P, R]":
		"""
		Unsubscribe a handler from this event.

		:param handler: The handler to unsubscribe.
		:type handler: Callable[P, Awaitable[None]]
		:return: The event instance.
		:rtype: Event[P, Awaitable[None]]
		"""

	@overload
	def __call__(self: "Event[P, Awaitable[None]]", *args: P.args, **kwargs: P.kwargs) -> Coroutine[Any, Any, None]: ...
	# Docstring left blank to allow inheritance from function

	@overload
	def __call__(self: "Event[P, None]", *args: P.args, **kwargs: P.kwargs) -> None: ...
	# Docstring left blank to allow inheritance from function

	on_subscribe: "Event[[Event[P, R], Callable[P, None | Awaitable[None]]], None]"
	"""
	An event that is invoked when a handler subscribes to this event.

	This event cannot be overwritten.
	"""

	on_unsubscribe: "Event[[Event[P, R], Callable[P, None | Awaitable[None]]], None]"
	"""
	An event that is invoked when a handler unsubscribes from this event.
	
	This event cannot be overwritten.
	"""

def event(func: Callable[Concatenate[Any, P], R]) -> "Event[P, R]":
	"""
	Create an Event from a instance or class method.

	:param func: A callable to define the signature of the event.
	:type func: Callable[Concatenate[Any, P], R]
	:return: An Event with the same signature as the method without the instance or class parameter.
	:rtype: Event[P, R]
	:raises TypeError: If func is not Callable.
	"""