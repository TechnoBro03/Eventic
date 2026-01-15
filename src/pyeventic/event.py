import asyncio
import inspect
import threading
from typing import Any, AsyncContextManager, Awaitable, Callable, Concatenate, ContextManager, Coroutine, Generic, ParamSpec, TypeVar
from weakref import WeakKeyDictionary
from .awaitable_group import AwaitableGroup

P = ParamSpec("P")
R = TypeVar("R", None, Awaitable[None])

class _ContextManager(Generic[P, R], ContextManager["Event[P, R]"], AsyncContextManager["Event[P, R]"]):
	"""A context manager to subscribe and unsubscribe a handler to an Event."""
	def __init__(self, event: "Event[P, R]", handler: Callable[P, None | Awaitable[None]]) -> None:
		self._event = event
		self._handler = handler

	def __enter__(self) -> "Event[P, R]":
		self._event.subscribe(self._handler)
		return self._event

	def __exit__(self, exc_type: type | None, exc_value: BaseException | None, traceback: object | None) -> None:
		self._event.unsubscribe(self._handler)

	async def __aenter__(self) -> "Event[P, R]":
		return self.__enter__()

	async def __aexit__(self, exc_type: type | None, exc_value: BaseException | None, traceback: object | None) -> None:
		self.__exit__(exc_type, exc_value, traceback)

class Event(Generic[P, R]):
	__slots__ = ("_handlers", "_lock", "_func", "_on_subscribe", "_on_unsubscribe", "_events", "_owner", "_name", "_tasks")

	def __init__(self, func: Callable[P, R] | None = None, *, owner: type | None = None, name: str | None = None) -> None:
		if func and not callable(func): raise TypeError(f"Expected a callable, got {type(func).__name__!r}.")

		self._lock = threading.RLock()
		"""A reentrant lock to synchronize access to the handlers set."""

		self._handlers: set[Callable[P, None | Awaitable[None]]] = set()
		"""A set of handlers subscribed to this event."""

		self._events = WeakKeyDictionary[object, "Event[P, R]"]()
		"""The per-instance events for this event descriptor."""

		self._func = func
		"""The function wrapped with this event (if any)."""

		self._on_subscribe: "Event[[Event[P, R], Callable[P, None | Awaitable[None]]], None] | None" = None
		"""An event that is invoked when a handler is subscribed to this event."""

		self._on_unsubscribe: "Event[[Event[P, R], Callable[P, None | Awaitable[None]]], None] | None" = None
		"""An event that is invoked when a handler is unsubscribed from this event."""

		self._owner: type | None = owner
		"""The owner class of this event descriptor."""

		self._name: str | None = name
		"""The name of this event descriptor."""

		self._tasks: set[asyncio.Task[None]] = set()
		"""A set of currently running tasks for this event."""

	def __repr__(self) -> str:
		func = self._func.__name__ if self._func else "None"
		
		if self._owner and self._name:
			return f"<Event '{self._owner.__name__}.{self._name}' func={func!r} handlers={len(self)} tasks={len(self._tasks)}>"
		else:
			return f"<Event func={func!r} handlers={len(self)} tasks={len(self._tasks)}>"

	def __str__(self) -> str:
		if self._owner and self._name:
			return f"Event('{self._owner.__name__}.{self._name}')"
		return f"Event({self._func.__name__ if self._func else None!r})"
	
	def __len__(self) -> int:
		with self._lock: return len(self._handlers)

	def __set_name__(self, owner: type, name: str) -> None:
		"""
		Set the owner and name of the descriptor when assigned to a class attribute.

		:param owner: The class where the descriptor is being assigned.
		:type owner: type
		:param name: The attribute name to which the descriptor is being assigned.
		:type name: str
		"""
		self._owner = owner
		self._name = name

	def __get__(self, instance: object | None, owner: type) -> "Event[P, R]":
		"""
		Get the event for the specific instance or class.

		:param instance: The instance where the event is being accessed, or None if accessed from the class.
		:type instance: object | None
		:param owner: The class where the descriptor is being accessed.
		:type owner: type
		:return: The Event for the specific instance or class.
		:rtype: Event[P, R]
		"""
		# Descriptor access from the class, return the descriptor itself
		if instance is None: return self

		# Descriptor access from an instance, return the per-instance event
		with self._lock:
			event = self._events.setdefault(instance, Event[P, R](self._func, owner=self._owner, name=self._name))
		return event

	def __set__(self, instance: object, value: "Event[P, R]") -> None:
		"""
		Set the event for the specific instance.

		:param instance: The instance where the event is being set.
		:type instance: object
		:param value: The Event to set.
		:type value: "Event[P, R]"
		"""
		# Do nothing to prevent overwriting the descriptor

	def subscribe(self, handler: Callable[P, None | Awaitable[None]]) -> Callable[P, None | Awaitable[None]]:
		if not callable(handler): raise TypeError(f"Expected a callable, got {type(handler).__name__!r}.")

		with self._lock:
			if handler not in self._handlers:
				self._handlers.add(handler)
				self.on_subscribe(self, handler)
		return handler
	
	def unsubscribe(self, handler: Callable[P, None | Awaitable[None]]) -> None:
		if not callable(handler): raise TypeError(f"Expected a callable, got {type(handler).__name__!r}.")

		with self._lock:
			if handler in self._handlers:
				self._handlers.remove(handler)
				self.on_unsubscribe(self, handler)
		return None
	
	def invoke(self, *args: P.args, **kwargs: P.kwargs) -> AwaitableGroup:
		with self._lock:
			handlers = list(self._handlers)
		awaitables: list[Awaitable[None]] = []

		for handler in handlers:
			try:
				result = handler(*args, **kwargs)
				if result and inspect.isawaitable(result):
					awaitables.append(result)
			except Exception: pass # Ignore exceptions in handlers

		# Always return an awaitable, even if there are no awaitables to run.
		# Acts as None for synchronous handlers and a coroutine for asynchronous ones
		return AwaitableGroup(*awaitables)
	
	def fire(self: "Event[P, Awaitable[None]]", *args: P.args, **kwargs: P.kwargs) -> asyncio.Task[None]:
		awaitable = self.invoke(*args, **kwargs)

		try:
			# Schedule the coroutine in the running event loop
			task = asyncio.create_task(awaitable)
			# In case of task cancellation or error, close the coroutine to prevent warnings
			task.add_done_callback(lambda t: awaitable.close())

			# Track the task to be able to wait for it later
			with self._lock:
				self._tasks.add(task)
				task.add_done_callback(self._on_task_done)

			return task
		except RuntimeError:
			# No running event loop, close the coroutine to prevent warnings
			awaitable.close()
			raise RuntimeError("No running event loop; cannot schedule handlers.")

	async def wait(self) -> None:
		with self._lock:
			tasks = list(self._tasks)

		if tasks:
			await asyncio.gather(*tasks, return_exceptions=True)

	def once(self, handler: Callable[P, None | Awaitable[None]]) -> Callable[P, None | Awaitable[None]]:
		if not callable(handler): raise TypeError(f"Expected a callable, got {type(handler).__name__!r}.")

		def wrapper(*args: P.args, **kwargs: P.kwargs) -> None | Awaitable[None]:
			self.unsubscribe(wrapper)
			return handler(*args, **kwargs)

		self.subscribe(wrapper)
		return wrapper
	
	def subscribed(self, handler: Callable[P, None | Awaitable[None]]) -> _ContextManager[P, R]:
		if not callable(handler): raise TypeError(f"Expected a callable, got {type(handler).__name__!r}.")
		return _ContextManager(self, handler)

	def __iadd__(self, handler: Callable[P, None | Awaitable[None]]) -> "Event[P, R]":
		self.subscribe(handler)
		return self

	def __isub__(self, handler: Callable[P, None | Awaitable[None]]) -> "Event[P, R]":
		self.unsubscribe(handler)
		return self
	
	def __call__(self, *args: P.args, **kwargs: P.kwargs) -> AwaitableGroup:
		return self.invoke(*args, **kwargs)
	
	@property
	def on_subscribe(self) -> "Event[[Event[P, R], Callable[P, None | Awaitable[None]]], None]":
		with self._lock:
			if self._on_subscribe is None: self._on_subscribe = Event()
		return self._on_subscribe
	
	@on_subscribe.setter
	def on_subscribe(self, value: "Event[[Event[P, R], Callable[P, None | Awaitable[None]]], None]") -> None: ...
	# Do nothing to prevent overwriting the event

	@property
	def on_unsubscribe(self) -> "Event[[Event[P, R], Callable[P, None | Awaitable[None]]], None]":
		with self._lock:
			if self._on_unsubscribe is None: self._on_unsubscribe = Event()
		return self._on_unsubscribe
	
	@on_unsubscribe.setter
	def on_unsubscribe(self, value: "Event[[Event[P, R], Callable[P, None | Awaitable[None]]], None]") -> None: ...
	# Do nothing to prevent overwriting the event

	def _on_task_done(self, task: asyncio.Task[None]) -> None:
		try: task.exception()
		except (Exception, asyncio.CancelledError): pass
		with self._lock:
			self._tasks.discard(task)

def event(func: Callable[Concatenate[Any, P], R]) -> "Event[P, R]":
	return Event[P, R](func) # type: ignore # This is for typing only, callable is never used
