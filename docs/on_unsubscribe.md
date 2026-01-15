# on_unsubscribe

An event that is invoked when a handler unsubscribes from this event.

```python
on_unsubscribe: Event[[Event[P, R], Callable[P, None | Awaitable[None]]], None]
```

## Parameters

* **event**: `Event[P, R]`\
The event being unsubscribed from.

* **callable**: `Event[P, R]`\
The callable being unsubscribed.

> [!NOTE]
> Although this is an attribute, it cannot be overwritten by direct assignment. Other event operations will work as intended (`+=`, `-=`, etc).

## Examples

```python
@Event
def event(value: int) -> None: ...

event.on_unsubscribe += lambda evt, handler: print(f"Handler {handler} unsubscribed from event {evt}")

@event.subscribe
def handler(value: int) -> None: ...

event.unsubscribe(handler)

# Output
# Handler <function handler at 0x000001540B70E660> unsubscribed from event Event('event')
```

```python
@Event
def event(value: int) -> None: ...
on = event.on_unsubscribe

# Direct assignment
event.on_unsubscribe = Event()

# Event remains unchanged
print(on is event.on_unsubscribe)

# Output:
# True
```
