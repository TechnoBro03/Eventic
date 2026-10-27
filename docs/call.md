# __call__ (`e(...)`)

Invoke this event with the given arguments.

```python
def __call__(self: Event[P,R], *args: P.args, **kwargs: P.kwargs) -> None | Coroutine[Any, Any, None]: ...
```

## Parameters

* **\*args**: `P.args`\
The positional arguments.

* **\*\*kwargs**: `P.kwargs`\
The keyword arguments.

## Returns

* `None | Coroutine[Any, Any, None]`

> [!IMPORTANT]
> * Handlers are called in the order they subscribed.
> * An exception raised by a handler does not stop the remaining handlers. It is passed to the event's `on_error` callback (see [\_\_init\_\_()](init.md)), or ignored if there is none.
> * Synchronous handlers are executed consecutively first, followed by the concurrent execution of asynchronous handlers. To avoid stalling the event loop, ensure synchronous handlers are non-blocking.
> * Asynchronous work is **NOT** scheduled, the returned Coroutine must be explicitly awaited to run asynchronous work.

> [!TIP]
> When an asynchronous event is invoked, it returns a `Coroutine`. While Coroutines are usually always "truthy," this specific Coroutine’s truthiness indicates whether there is actual asynchronous work that needs to be awaited. See [this example](#truthy).

## Overloads

```python
@overload
def __call__(self: Event[P, None], *args: P.args, **kwargs: P.kwargs) -> None: ...

@overload
def __call__(self: Event[P, Awaitable[None]], *args: P.args, **kwargs: P.kwargs) -> Coroutine[Any, Any, None]: ...
```

## Examples

```python
@event
def my_event(value: int, text: str, /) -> None: ...

# Synchronous invocation
my_event(42, "Hello, World!")
```

```python
@event
async def my_event(value: int, text: str, /) -> None: ...

async def main():
    # Asynchronous invocation
    # The returned Coroutine must be assigned to a variable or awaited
    await my_event(42, "Hello, World!")
```

<div id="truthy"></div>

```python
@event
async def my_event(value: int, text: str, /) -> None: ...

async def main():
    if co := my_event(42, "Hello, World!"):
        # There are async handlers. We must await their completion.
        await co
    else:
        # Everything was synchronous and is already finished.
        pass
```
