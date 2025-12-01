from types import TracebackType
from typing import Any, Awaitable, Coroutine, Generator

class AwaitableGroup(Coroutine[Any, Any, None], Awaitable[None]):
	"""
	An awaitable coroutine that aggregates multiple awaitables and runs them concurrently.

	If the AwaitableGroup is closed or deleted, any pending awaitables are cleaned up to prevent warnings.
	"""
	def __init__(self, *awaitables: Awaitable[None]) -> None:
		"""
		Initialize a new AwaitableGroup with the given awaitables.

		:param awaitables: The awaitables to aggregate.
		:type awaitables: tuple[Awaitable[None], ...]
		"""

	def __bool__(self) -> bool:
		"""
		Return True if the AwaitableGroup has pending awaitables and is not closed.

		:return: True if there are pending awaitables and the group is not closed, False otherwise.
		:rtype: bool
		"""

	def __await__(self) -> Generator[Any, None, None]:
		"""
		Await the AwaitableGroup, running all contained awaitables concurrently.
		"""

	def send(self, value: Any) -> Any:
		"""
		Send a value into the AwaitableGroup's internal coroutine.

		:param value: The value to send.
		:return: The result of sending the value.
		"""

	def throw(self, typ: type[BaseException] | BaseException, val: BaseException | object = None, tb: TracebackType | None = None) -> Any:
		"""
		Throw an exception into the AwaitableGroup's internal coroutine.

		:param typ: The exception type or instance to throw.
		:param val: The exception value.
		:param tb: The traceback object.
		:return: The result of throwing the exception.
		"""

	def close(self) -> None:
		"""
		Close the AwaitableGroup, cancelling and closing any pending coroutine awaitables.
		"""