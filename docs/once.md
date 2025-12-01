# once

Subscribe a handler to this event that will be invoked only once.

```python
def once(self: Event[P, R], handler: Callable[P, None | Awaitable[None]]) -> Callable[P, None | Awaitable[None]]: ...
```

## Parameters

* **handler**: `Callable[P, None | Awaitable[None]]`\
The handler to subscribe.

## Returns

* `Callable[P, None | Awaitable[None]]`\
The wrapped callable.

## Raises

* `TypeError`\
**handler** is not `Callable`.

> [!TIP]
> To unsubscribe the handler before it is invoked, unsubscribe the **wrapped callable**.

## Overloads

```python
@overload
def once(self: Event[P, None], handler: Callable[P, None]) -> Callable[P, None]: ...

@overload
def once(self: Event[P, Awaitable[None]], handler: Callable[P, None]) -> Callable[P, None]: ...

@overload
def once(self: Event[P, Awaitable[None]], handler: Callable[P, Awaitable[None]]) -> Callable[P, Awaitable[None]]: ...
```

## Examples

```python
@Event
def event(value: int, text: str) -> None: ...

event.once(lambda value, text: print(f"handler: {value} {text}"))

event.invoke(1, "2")
event.invoke(3, "4")

# Output:
# handler: 1 2
```

```python
@Event
def event(value: int, text: str) -> None: ...

# Decorator
@event.once
def handler(value: int, text: str) -> None: print(f"handler: {value} {text}")

event.invoke(1, "2")
event.invoke(3, "4")

# Output
# handler: 1 2
```

```python
@Event
def event(value: int, text: str) -> None: ...

wrapper = event.once(lambda value, text: print(f"handler: {value} {text}"))
event.unsubscribe(wrapper)

event.invoke(1, "2")

# Output:
#
```
