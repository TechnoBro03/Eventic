import pytest
import inspect
from pyeventic import event

def test_signature_positional_only_and_keyword_only():
	@event
	def e1(a: int, b: str, /) -> None: ...
	@event
	def e2(*, a: int, b: str) -> None: ...
	@event
	def e3(a: int, /, *, b: str) -> None: ...

def test_signature_positional_or_keyword_forbidden():
	def prototype(a: int) -> None: ...

	with pytest.raises(TypeError, match="'a' must be positional-only or keyword-only"):
		event(prototype)

def test_signature_var_args_forbidden():
	def args(*args: int) -> None: ...
	def kwargs(**kwargs: int) -> None: ...

	with pytest.raises(TypeError, match=r"cannot be \*args or \*\*kwargs"):
		event(args)
	with pytest.raises(TypeError, match=r"cannot be \*args or \*\*kwargs"):
		event(kwargs)

def test_signature_defaults_forbidden():
	def prototype(a: int = 1, /) -> None: ...

	with pytest.raises(TypeError, match="'a' cannot have a default value"):
		event(prototype)

def test_signature_method_skips_self():
	class MyClass:
		@event(method=True)
		def e1(self, a: int, /) -> None: ...
		@event(method=True)
		def e2(self, *, a: int) -> None: ...

	with pytest.raises(TypeError, match="'a' must be positional-only"):
		class Bad:
			@event(method=True)
			def e(self, a: int) -> None: ...

def test_signature_unavailable():
	class NoSignature:
		def __call__(self) -> None: ...
		@property
		def __signature__(self) -> inspect.Signature: raise ValueError("No signature")

	event(NoSignature()) # Should not raise
