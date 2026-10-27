# event

Create an Event from a function, or from an instance or class method.

```python
def event(func: Callable[P, R], /) -> Event[P, R]: ...
def event(*, method: Literal[False] = False, on_error: Callable[[Exception], None] | None = None) -> Callable[[Callable[P, R]], Event[P, R]]: ...
def event(*, method: Literal[True], on_error: Callable[[Exception], None] | None = None) -> Callable[[Callable[Concatenate[Any, P], R]], Event[P, R]]: ...
```

## Parameters

* **func**: `Callable[P, R]`\
A callable to define the signature of the event.

* **method**: `bool`\
Whether **func** is an instance or class method. When `True`, the first parameter (`self` / `cls`) is removed from the event signature and is not validated. Defaults to `False`.

* **on_error**: `Callable[[Exception], None] | None`\
Called with each exception raised by a handler. Defaults to `None`, which ignores them. See [Handling Exceptions](../README.md#handling-exceptions).

## Returns
* `Event[P, R]`\
An Event with the same signature as **func**.

* `Callable[[Callable[P, R]], Event[P, R]]`\
When called with options only, a decorator that creates the Event. With `method=True`, the Event's signature does not include the instance or class parameter.

## Raises

* `TypeError`\
**func** or **on_error** is not `Callable`, or the signature of **func** breaks a rule (see below).

> [!TIP]
> The passed function is never executed; it serves strictly as a type hint signature. To keep your code clean, it is recommended to use an empty function body (`pass` or `...`).

> [!IMPORTANT]
> The signature of **func** is checked when the event is created:
> * Every parameter must be positional-only (before `/`) or keyword-only (after `*`), so handlers know how arguments will be passed.
> * Parameters cannot have default values, since it would be unclear whether handlers receive them.
> * `*args` and `**kwargs` are not allowed.

> [!NOTE]
> `event` is the only way to create an Event from a function. `Event` itself only takes options (see [\_\_init\_\_()](init.md)), so `@Event` and `Event(func)` raise a `TypeError`.

## Examples

```python
# Decorator
@event
def on_save(path: str, /) -> None: ...

on_save.invoke("notes.txt")
```

```python
def signature(value: int, /) -> None:
	"""
	An example event signature.

	:param value: An example value.
	"""

# Function call, with or without options
on_change = event(signature)
on_change_reported = event(signature, on_error=print)
```

```python
# Decorator with options
@event(on_error=print)
def on_move(x: int, y: int, /) -> None: ...
```

```python
class MyClass:
    # Method decorator, does not expect self as first parameter
    @event(method=True)
    def my_event(self, value: int, /) -> None: ...

MyClass.my_event.invoke(5)
```

```python
class MyClass:
    # Method decorator with options
    @event(method=True, on_error=print)
    def my_event(self, *, value: int) -> None: ...

MyClass.my_event.invoke(value=5)
```

```python
class MyClass:
    # A staticmethod has no instance parameter, so method=True is not needed
    @event
    @staticmethod
    def my_event(value: int, /) -> None: ...

MyClass.my_event.invoke(5)
```

```python
class MyClass:
    # Without method=True, self is part of the event signature and is passed by the caller
    @event
    def my_event(self, value: int, /) -> None: ...

instance = MyClass()
MyClass.my_event.invoke(instance, 5)
```
