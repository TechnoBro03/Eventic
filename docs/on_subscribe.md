# on_subscribe

An event that is invoked when a handler subscribes to this event.

```python
on_subscribe: Event[[Event[P, R], Callable[P, None | Awaitable[None]]], None]
```

## Parameters

* **event**: `Event[P, R]`\
The event being subscribed to.

* **callable**: `Event[P, R]`\
The callable being subscribed.

> [!NOTE]
> Although this is an attribute, it cannot be overwritten by direct assignment. Other event operations will work as intended (`+=`, `-=`, etc).

## Examples

```python
@Event
def event(value: int) -> None: ...

event.on_subscribe += lambda evt, handler: print(f"Handler {handler} subscribed to event {evt}")

@event.subscribe
def handler(value: int) -> None: ...

# Output
# Handler <function handler at 0x0000011B61CCE660> subscribed to event Event('event')
```

```python
@Event
def event(value: int) -> None: ...
on = event.on_subscribe

# Direct assignment
event.on_subscribe = Event()

# Event remains unchanged
print(on is event.on_subscribe)

# Output:
# True
```
