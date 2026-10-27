# \_\_repr\_\_ (`repr(e)`)

Return a detailed string representation of this Event.

Includes the bound function name (if any), owner class and attribute name (if any), and number of subscribed handlers and background tasks.

```python
def __repr__() -> str: ...
```

## Returns

* `str`\
The detailed string representation of this Event.

## Examples

```python
class MyClass:
    @event(method=True)
    def my_event(self, value: int, /) -> None: ...

print(repr(MyClass.my_event))

# Output:
# <Event 'MyClass.my_event' func='my_event' handlers=0 tasks=0>
```