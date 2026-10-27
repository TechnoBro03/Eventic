# subscribed

Get a context manager that subscribes a handler to this event upon entering the context and unsubscribes it upon exiting.

```python
def subscribed(self: Event[P, R], handler: Callable[P, None | Awaitable[None]]) -> ContextManager[Event[P, None]] | AsyncContextManager[Event[P, Awaitable[None]]]: ...
```

## Parameters

* **handler**: `Callable[P, None | Awaitable[None]]`\
The handler to subscribe.

## Returns

* `ContextManager[Event[P, None]] | AsyncContextManager[Event[P, Awaitable[None]]]`\
A context manager for the subscription.

## Raises

* `TypeError`\
**handler** is not `Callable`.

## Overloads

```python
@overload
def subscribed(self: Event[P, None], handler: Callable[P, None]) -> ContextManager[Event[P, None]]: ...

@overload
def subscribed(self: Event[P, Awaitable[None]], handler: Callable[P, None]) -> AsyncContextManager[Event[P, Awaitable[None]]]: ...

@overload
def subscribed(self: Event[P, Awaitable[None]], handler: Callable[P, Awaitable[None]]) -> AsyncContextManager[Event[P, Awaitable[None]]]: ...
```

## Examples

```python
@event
def my_event(value: int, text: str, /) -> None: ...

with my_event.subscribed(lambda value, text: print(f"handler: {value} {text}")):
    my_event.invoke(1, "2")

my_event.invoke(3, "4")

# Output:
# handler 1 2
```

```python
@event
async def my_event(value: int, text: str, /) -> None: ...

async def main():
    async with my_event.subscribed(lambda value, text: print(f"handler: {value} {text}")):
        await my_event.invoke(1, "2")

    await my_event.invoke(3, "4")

# Output:
# handler: 1 2
```
