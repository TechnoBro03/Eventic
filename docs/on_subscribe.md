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
@event
def my_event(value: int, /) -> None: ...

my_event.on_subscribe += lambda evt, handler: print(f"Handler {handler} subscribed to event {evt}")

@my_event.subscribe
def handler(value: int) -> None: ...

# Output
# Handler <function handler at 0x0000011B61CCE660> subscribed to event Event('my_event')
```

```python
@event
def my_event(value: int, /) -> None: ...
on = my_event.on_subscribe

# Direct assignment
my_event.on_subscribe = Event()

# Event remains unchanged
print(on is my_event.on_subscribe)

# Output:
# True
```
