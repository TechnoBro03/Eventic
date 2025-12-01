# wait

Wait for all currently running event invocations to complete.

```python
def wait(self: Event[P, Awaitable[None]]) -> Coroutine[Any, Any, None]: ...
```

## Returns

* `Coroutine[Any, Any, None]`

> [!TIP]
> When firing multiple events, use the wait function to ensure the next action only executes once all previous processes have finished.

## Examples

```python
@Event
async def event(value: int, text: str) -> None: ...

async def slow_handler(value: int, text: str) -> None:
    await asyncio.sleep(1)
    print(f"slow handler: {value} {text}")

async def fast_handler(value: int, text: str) -> None:
    print(f"fast handler: {value} {text}")

async def main():
    event.subscribe(slow_handler)
    event.fire(42, "Hello, World!")

    event.subscribe(fast_handler)

    # Wait for all previous processes to finish
    await event.wait()
    await event.fire(100, "Goodbye!")

# Output:
# slow handler: 42 Hello, World!
# fast handler: 100 Goodbye!
# slow handler: 100 Goodbye
```