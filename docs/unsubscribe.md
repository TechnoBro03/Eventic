# unsubscribe

Unsubscribe a handler from this event.

```python
def unsubscribe(self: Event[P, R], handler: Callable[P, None | Awaitable[None]]) -> None: ...
```

## Parameters

* **handler**: `Callable[P, None | Awaitable[None]]`\
The handler to subscribe.

## Returns

* `None`

## Raises

* `TypeError`\
**handler** is not `Callable`.

> [!NOTE]
> If the handler is not already subscribed, this method does nothing.

## Overloads

```python
@overload
def unsubscribe(self: Event[P, None], handler: Callable[P, None]) -> None: ...

@overload
def unsubscribe(self: Event[P, Awaitable[None]], handler: Callable[P, None]) -> None: ...

@overload
def unsubscribe(self: Event[P, Awaitable[None]], handler: Callable[P, Awaitable[None]]) -> None: ...
```

## Examples

```python
@Event
def event(value: int, text: str) -> None: ...

def handler(value: int, text: str) -> None:
	print(f"handler: {value} {text}")

# Method call
event.unsubscribe(handler)
```
