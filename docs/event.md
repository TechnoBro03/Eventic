# event

Create an Event from a instance or class method.

```python
def event(func: Callable[Concatenate[Any, P], R]) -> Event[P, R]:
```

## Parameters

* **func**: `Concatenate[Any, P], R]`\
A callable to define the signature of the event.

## Returns
* `Event[P, R]`\
An Event with the same signature as the method without the instance or class parameter.

## Raises

* `TypeError`\
**func** is not `Callable`.

> [!TIP]
> The passed function is never executed; it serves strictly as a type hint signature. To keep your code clean, it is recommended to use an empty function body (`pass` or `...`).

## Examples

```python
class MyClass:
    def event_signature(self, value: int) -> None: ...
	event = event(event_signature)

# Does not expect self as first parameter
MyClass.event.invoke(5)
```

```python
class MyClass:
    # Decorator
    @event
    def event(self, value: int) -> None: ...

# Does not expect self as first parameter
MyClass.event.invoke(5)
```