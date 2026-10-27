# \_\_init\_\_

Initialize a new Event.

```python
def __init__(*, on_error: Callable[[Exception], None] | None = None) -> None: ...
```

## Parameters

* **on_error**: `Callable[[Exception], None] | None`\
Called with each exception raised by a handler. Defaults to `None`, which ignores them. See [Handling Exceptions](../README.md#handling-exceptions).

## Raises

* `TypeError`\
A function was passed (use [event()](event.md) to create an Event from a function), or **on_error** is not `Callable`.

> [!TIP]
> The signature is given with type arguments (`Event[[int], None]()`). To define it with a function instead, which also gives the event a docstring, use [event()](event.md). `@Event` is not supported, use `@event`.

> [!NOTE]
> Without type arguments, `Event()` is a synchronous event with no parameters (`Event[[], None]`).

## Examples

```python
# Synchronous event with no parameters
my_event = Event()
```

```python
# Manual definition (strong typing, no docstring)
my_event = Event[[int], None]()
```

```python
# Type arguments from an annotation
my_event: Event[[int], None] = Event()
```

```python
# Manual definition with options
my_event = Event[[int], None](on_error=print)
```

```python
# Asynchronous event
my_event = Event[[int], Awaitable[None]]()
```
