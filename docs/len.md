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
@event
def my_event(value: int, /) -> None: ...

my_event += lambda value: print("lambda 1")
my_event += lambda value: print("lambda 2")
my_event += lambda value: print("lambda 3")

print(len(my_event))

# Output
# 3
```