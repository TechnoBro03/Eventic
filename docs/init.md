# \_\_init\_\_

Initialize a new Event.

```python
def __init__(func: Callable[P, R] | None = None) -> None: ...
```

## Parameters

* **func**: `Callable[P, R]`\
An optional function to define the signature of the event.

## Raises

* `TypeError`\
**func** is not `Callable` or `None`.

> [!TIP]
> The passed function is never executed; it serves strictly as a type hint signature. To keep your code clean, it is recommended to use an empty function body (`pass` or `...`).

## Examples

```python
# Manual definition (no typing or docstring)
event = Event()
```

```python
# Manual definition (strong typing, no docstring)
event = Event[[int], None]()
```

```python
def signature(value: int) -> None:
	"""
	An example event signature.

	:param value: An example value.
	"""

# Function definition (strong typing and docstring)
event = Event(signature)
```

```python
# Decorator definition (strong typing and docstring)
@Event
def event(value: int) -> None:
	"""
	An example event signature.

	:param value: An example value.
	"""
```

> [!TIP]
> When working with events in a class, many type checkers expect the first argument of a method to be "self". If that is the desired behavior, great! If not, below are some ways to resolve that warning while still providing the desired signature:

```python
class MyClass:
    @Event
    def event1(value: int) -> None: ...
    # Error: Type of parameter "value" must be a supertype of its class "MyClass"

    @Event
    def event2(self, value: int) -> None: ...
    # No error here, as "self" is expected, error will be raised when invoking

    @Event
    def event3(value: int) -> None: ... # type: ignore
    # This will ignore the type error

    @Event
    @staticmethod
    def event4(value: int) -> None: ...
    # No error

    @event
    def event5(self, value: int) -> None: ...
    # No error
    # Using the "event" decorator instead of the "Event" decorator will not error and removes "self" from the event signature.

MyClass.event1.invoke(1)
# No error

MyClass.event2.invoke(2)
# Error: Argument of type "2" cannot be assigned to parameter "self" of type "MyClass" in function "invoke"

MyClass.event3.invoke(3)
# No error

MyClass.event4.invoke(4)
# No error

MyClass.event5.invoke(5)
# No error
```

> [!TIP]
> See [event()](docs/event.md) to learn more about the event method.