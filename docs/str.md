# \_\_str\_\_ (`str(e)`)

Return a user-friendly string representation of this Event.

```python
def __str__() -> str: ...
```

## Returns

* `str`\
The user-friendly string representation of this Event.

## Examples

```python
class MyClass:
    @event
    def event(self, value: int) -> None: ...

print(str(MyClass.event))

# Output:
# Event('MyClass.event')
```