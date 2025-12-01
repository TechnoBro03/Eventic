# invoke

Invoke this event with the given arguments.

```python
def invoke(self: Event[P,R], *args: P.args, **kwargs: P.kwargs) -> None | Coroutine[Any, Any, None]: ...
```

## Parameters

* **\*args**: `P.args`\
The positional arguments.

* **\*\*kwargs**: `P.kwargs`\
The keyword arguments.

## Returns

* `None | Coroutine[Any, Any, None]`

> [!IMPORTANT]
> * Individual handler exceptions are suppressed to ensure the event chain completes. Handlers should implement their own `try/except` blocks to manage internal exceptions.
> * Synchronous handlers are executed consecutively first, followed by the concurrent execution of asynchronous handlers. To avoid stalling the event loop, ensure synchronous handlers are non-blocking.
> * Asynchronous work is **NOT** scheduled, the returned Coroutine must be explicitly awaited to run asynchronous work.

> [!TIP]
> When an asynchronous event is invoked, it returns a `Coroutine`. While Coroutines are usually always "truthy," this specific Coroutine’s truthiness indicates whether there is actual asynchronous work that needs to be awaited. See [this example](#truthy).

## Overloads

```python
@overload
def invoke(self: Event[P, None], *args: P.args, **kwargs: P.kwargs) -> None: ...

@overload
def invoke(self: Event[P, Awaitable[None]], *args: P.args, **kwargs: P.kwargs) -> Coroutine[Any, Any, None]: ...
```

## Examples

```python
@Event
def event(value: int, text: str) -> None: ...

# Synchronous invocation
event.invoke(42, "Hello, World!")
```

```python
@Event
async def event(value: int, text: str) -> None: ...

async def main():
    # Asynchronous invocation
    # The returned Coroutine must be assigned to a variable or awaited
    await event.invoke(42, "Hello, World!")
```
<div id="truthy"></div>

```python
@Event
async def event(value: int, text: str) -> None: ...

async def main():
    if co := event.invoke(42, "Hello, World!"):
        # There are async handlers. We must await their completion.
        await co
    else:
        # Everything was synchronous and is already finished.
        pass
```
