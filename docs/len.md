# \_\_len\_\_ (`len(e)`)

Return the number of handlers subscribed to this event.

```python
def __len__() -> int: ...
```

## Returns

* `int`\
The number of subscribed handlers.

## Examples

```python
@Event
def event(value: int) -> None: ...

event += lambda value: print("lambda 1")
event += lambda value: print("lambda 2")
event += lambda value: print("lambda 3")

print(len(event))

# Output
# 3
```