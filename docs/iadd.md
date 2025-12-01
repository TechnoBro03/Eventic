# \_\_iadd\_\_ (`+=`)

Subscribe a handler to this event.

```python
def __iadd__(self: Event[P, R], handler: Callable[P, None | Awaitable[None]]) -> Event[P, R]: ...
```

## Parameters

* **handler**: `Callable[P, None | Awaitable[None]]`\
The handler to subscribe.

## Returns

* `Event[P, R]`\
The event instance.

## Raises

* `TypeError`\
**handler** is not `Callable`.

> [!NOTE]
> * The handler is invoked whenever the event is fired.
> * The order of invocation is not guaranteed.
> * A handler may only be subscribed once; subsequent subscriptions of the same handler have no effect.

## Overloads

```python
@overload
def __iadd__(self: Event[P, None], handler: Callable[P, None]) -> Event[P, None]: ...

@overload
def __iadd__(self: Event[P, Awaitable[None]], handler: Callable[P, None]) -> Event[P, Awaitable[None]]: ...

@overload
def __iadd__(self: Event[P, Awaitable[None]], handler: Callable[P, Awaitable[None]]) -> Event[P, Awaitable[None]]: ...
```

## Examples

```python
@Event
def event(value: int, text: str) -> None: ...

def handler(value: int, text: str) -> None:
	print(f"handler: {value} {text}")

event += handler
```

```python
@Event
def event(value: int, text: str) -> None: ...

# Lambda
event += lambda value, text: print(f"lambda handler: {value} {text}")
```
