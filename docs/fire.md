# fire

Invoke this event with the given arguments and schedule the handlers to run.

```python
def fire(self: Event[P,Awaitable[None]], *args: P.args, **kwargs: P.kwargs) -> Task[None]: ...
```

## Parameters

* **\*args**: `P.args`\
The positional arguments.

* **\*\*kwargs**: `P.kwargs`\
The keyword arguments.

## Returns

* `Task[None]`

> [!IMPORTANT]
> * Individual handler exceptions are suppressed to ensure the event chain completes. Handlers should implement their own `try/except` blocks to manage internal exceptions.
> * Synchronous handlers are executed consecutively first, followed by the concurrent execution of asynchronous handlers. To avoid stalling the event loop, ensure synchronous handlers are non-blocking.
> * Asynchronous work **is** scheduled on the event loop without the need to await (ie. fire and forget).

## Examples

```python
@Event
async def event(value: int, text: str) -> None: ...

async def handler(value: int, text: str) -> None:
    await asyncio.sleep(.5)
    print(f"handler: {value} {text}")

async def main():
    event.subscribe(handler)

    # Fire and forget, do not need to capture or await the task, but can if desired
    task = event.fire(42, "Hello, World!")

    # The task is not being awaited, but we sleep to allow the event to process
    await asyncio.sleep(1)

asyncio.run(main())

# Output:
# handler: 42 Hello, World
```