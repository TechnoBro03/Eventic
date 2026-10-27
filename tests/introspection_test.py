import inspect
from pyeventic import event

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
