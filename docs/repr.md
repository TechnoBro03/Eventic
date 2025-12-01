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
    @event
    def event(self, value: int) -> None: ...

print(repr(MyClass.event))

# Output:
# <Event 'MyClass.event' func='event' handlers=0 tasks=0>
```