import asyncio
import inspect
from types import TracebackType
from typing import Any, Awaitable, Coroutine, Generator

class AwaitableGroup(Coroutine[Any, Any, None], Awaitable[None]):
	def __init__(self, *awaitables: Awaitable[None]) -> None:
		self._awaitables: list[Awaitable[None]] = list(awaitables)

		self._disposed: bool = False

		self._coroutine: Coroutine[Any, Any, None] | None = None
		self._iter: Generator[Any, None, None] | None = None

	def __bool__(self) -> bool:
		return not self._disposed and bool(self._awaitables)

	async def _runner(self) -> None:
		if not self._awaitables: return
		try: await asyncio.gather(*self._awaitables, return_exceptions=True)
		finally: self.close()

	@property
	def _iterator(self) -> Generator[Any, None, None]:
		if self._disposed: raise RuntimeError("EventInvocation has been closed.")
		if self._iter is None:
			self._coroutine = self._runner()
			self._iter = self._coroutine.__await__()
		return self._iter

	def __await__(self) -> Generator[Any, None, None]:
		return self._iterator

	def send(self, value: Any) -> Any:
		return self._iterator.send(value)

	def throw(self, typ: type[BaseException] | BaseException, val: BaseException | object = None, tb: TracebackType | None = None) -> Any:
		return self._iterator.throw(typ)

	def close(self) -> None:
		if self._disposed: return
		self._disposed = True

		awaitables = list(self._awaitables)
		self._awaitables.clear()

		for a in awaitables:
			if inspect.iscoroutine(a):
				try: a.close()
				except Exception: ...

		# Close the internal iterator/coroutine
		try: self._iter.close() if self._iter else None
		except Exception: ...
		try: self._coroutine.close() if self._coroutine else None
		except Exception: ...

	def __del__(self) -> None:
		self.close()