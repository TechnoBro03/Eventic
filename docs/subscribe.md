# subscribe

Subscribe a handler to this event.

```python
def subscribe(self: Event[P, R], handler: Callable[P, None | Awaitable[None]]) -> Callable[P, None | Awaitable[None]]: ...
```

## Parameters

* **handler**: `Callable[P, None | Awaitable[None]]`\
The handler to subscribe.

## Returns

* `Callable[P, None | Awaitable[None]]`\
The original callable.

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
def subscribe(self: Event[P, None], handler: Callable[P, None]) -> Callable[P, None]: ...

@overload
def subscribe(self: Event[P, Awaitable[None]], handler: Callable[P, None]) -> Callable[P, None]: ...

@overload
def subscribe(self: Event[P, Awaitable[None]], handler: Callable[P, Awaitable[None]]) -> Callable[P, Awaitable[None]]: ...
```

## Examples

```python
# Assuming you have the following Event defined:
@Event
def event(value: int, text: str) -> None: ...
```

```python
def handler1(value: int, text: str) -> None:
	print(f"handler1: {value} {text}")

# Method call
event.subscribe(handler1)
```

```python
# Decorator
@event.subscribe
def handler2(value: int, text: str) -> None:
	print(f"handler2: {value} {text}")
```

```python
# Lambda
event.subscribe(lambda value, text: print(f"lambda handler {value}, {text}"))
```
