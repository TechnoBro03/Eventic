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
    @event(method=True)
    def my_event(self, value: int, /) -> None: ...

print(str(MyClass.my_event))

# Output:
# Event('MyClass.my_event')
```