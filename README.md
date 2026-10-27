# Eventic

[![Version](https://img.shields.io/pypi/v/pyeventic)](https://pypi.org/project/pyeventic/)
![Python](https://img.shields.io/pypi/pyversions/pyeventic)
![Coverage](https://img.shields.io/badge/coverage-100%25-success)
![MyPy](https://img.shields.io/badge/mypy-checked-blue)
![License](https://img.shields.io/github/license/TechnoBro03/Eventic)

A high-performance, strongly-typed event library for Python supporting both synchronous and asynchronous events.\
Eventic provides an easy way to implement the event pattern with full IDE support and thread safety.

## Table of Contents
- [Eventic](#eventic)
- [Table of Contents](#table-of-contents)
- [Features](#features)
- [Installation](#installation)
- [API Reference](#api-reference)
  - [Methods](#methods)
  - [Attributes](#attributes)
  - [Generics](#generics)
  - [Other](#other)
- [Strong Typing](#strong-typing)
- [Getting Started](#getting-started)
  - [The Basics](#the-basics)
  - [Asynchronous Tasks](#asynchronous-tasks)
    - [Blocking Tasks](#blocking-tasks-with-invoke-or-)
    - [Non-Blocking Tasks](#non-blocking-tasks-with-fire)
  - [Managing Subscriptions](#managing-subscriptions)
    - [Once](#once)
    - [Context Manager](#context-manager)
  - [Events within Classes](#events-within-classes)
  - [Subscribe Hooks](#subscribe-hooks)
  - [Event Options](#event-options)
  - [Signature Rules](#signature-rules)
  - [Handling Exceptions](#handling-exceptions)

## Features
* **Type Safety**: Strongly typed, fully compatible with many type checkers, with autocomplete for event signatures.
* **Unambiguous Signatures**: Event signatures are validated at definition time, so handlers always know whether arguments arrive by position or by name.
* **Isolated Handlers**: An exception in one handler never stops the others. Pass an `on_error` callback to see them.
* **Predictable Order**: Handlers are called in the order they subscribed.
* **Lifecycle Management**: Built in lifecycle event hooks allow you to easily manage resources only when listeners are present.
* **Flexible Invocation**: Choose between `invoke()` (awaitable), `fire()` (background execution), and standard call syntax `()`.
* **Sync/Async**: Handle both synchronous and asynchronous events and handlers.
* **One-Time Listeners**: Use `once()` to automatically unsubscribe after first execution. Perfect for initialization logic.
* **Scoped Subscriptions**: Use context managers (`with event.subscribed(...)`) to ensure handlers are cleaned up automatically.
* **Zero Dependencies**: A lightweight, pure Python implementation with no external requirements, making it easy to use in any project.
* **Descriptor Support**: Automatic per-instance event creation when used as a class attribute.
* **Thread-Safe**: Safe to use in multi-threaded environments.
* **Memory Safe**: No memory leaks or "forgotten" background tasks.
* **No Warning Pollution**: No `RuntimeWarning` warnings for un-awaited coroutines.

## Installation

1. Make sure `pip` is installed on your system.
2. Run the following command
	```bash
	pip install pyeventic
	```
> [!TIP]
> See [here](https://packaging.python.org/en/latest/tutorials/installing-packages/) for more details on installing packages.

## API Reference

### Methods

| Method | Description |
| --- | --- |
| [\_\_init\_\_()](docs/init.md) | Initialize a new Event. |
| [subscribe()](docs/subscribe.md) | Subscribe to this event. |
| [unsubscribe()](docs/unsubscribe.md) | Unsubscribe from this event. |
| [invoke()](docs/invoke.md) | Invoke the event. |
| [fire()](docs/fire.md) | Invoke the event and schedule async work in the background. |
| [wait()](docs/wait.md) | Waits for all background tasks to complete. |
| [once()](docs/once.md) | Subscribe to this event for a single invocation. |
| [subscribed()](docs/subscribed.md) | Context manager for temporary subscription. |
| [\_\_iadd\_\_() (`+=`)](docs/iadd.md) | Operator overload for subscribing to this event. |
| [\_\_isub\_\_() (`-=`)](docs/isub.md) | Operator overload for unsubscribing from this event. |
| [\_\_call\_\_() (`e()`)](docs/call.md) | Operator overload to invoke this event |
| [\_\_len\_\_() (`len(e)`)](docs/len.md) | Return the number of handlers subscribed to this event. |
| [\_\_str\_\_() (`str(e)`)](docs/str.md) | Return a user-friendly string representation of this event. |
| [\_\_repr\_\_() (`repr(e)`)](docs/repr.md) | Return a detailed string representation of this event. |

---

### Attributes

| Attribute | Description |
| --- | --- |
| [on_subscribe](docs/on_subscribe.md) | An event that is invoked when a handler subscribes to this event.|
| [on_unsubscribe](docs/on_unsubscribe.md) | An event that is invoked when a handler unsubscribes from this event. |

### Generics

| Variable | Type | Description |
| --- | --- | --- |
| P | ParamSpec | The signature of an Event. |
| R | TypeVar | The return type of an Event. `None` for synchronous Events, `Awaitable[None]` for asynchronous Events.. |

### Other

| Name | Type | Description |
| --- | --- | --- |
| [event()](docs/event.md) | Decorator | Create an Event from a function, or from an instance or class method with `method=True`. |

## Strong Typing

Eventic is a strongly typed library. This helps prevent runtime errors while writing your code, and provides nice feature like autocomplete and full docstring support.\
Below are a few examples of how the typing system works in Eventic (errors shown are from Pylance):

### Handler mismatch

```python
@event
def on_score_update(points: int, /) -> None: ...

@on_score_update.subscribe  # Error: handler signature does not match the event
def wrong_handler(points: str): ...

# Argument of type "(points: str) -> None" cannot be assigned to parameter "handler"
# of type "(points: int, /) -> None" in function "subscribe"
#   Parameter 1: type "int" is incompatible with type "str"
```

### Awaiting a sync event

```python
@event
def on_click(x: int, y: int, /) -> None: ...

async def main():
    await on_click(10, 20)  # Error: sync events return None

# "None" is not awaitable
```

### Not awaiting an async event

```python
@event
async def on_upload(file_id: str, /) -> None: ...

def trigger():
    on_upload("file_001")  # Error: async events must be awaited (or use .fire())

# Result of async function call is not used; use "await" or assign result to variable
```

### Passing the incorrect arguments to invoke

```python
@event
def update_score(points: int, /) -> None: ...

update_score("ten")  # Error: argument type does not match the event signature

# Argument of type "Literal['ten']" cannot be assigned to parameter "points" of type "int"
```

### Autocomplete and full docstring

```python
@event
def file_sent(path: str, size: int, encrypted: bool, /) -> None:
    """
    An event that is triggered when a file is sent.

    :param path: The file path.
    :type path: str
    :param size: The size of the file in bytes.
    :type size: int
    :param encrypted: Whether the file is encrypted.
    :type encrypted: bool
    """

file_sent("example.txt", 2048, True)
# Hovering or typing file_sent( shows the signature
#   (path: str, size: int, encrypted: bool, /) -> None
# along with the docstring and per-parameter descriptions above.
```


## Getting Started

### The Basics

An Event is a dispatcher. You can define a "template" for the event using type hints or function signatures, and then "subscribe" other functions that will be triggered when the event is fired.

Event parameters must be marked positional-only (`/`) or keyword-only (`*`), so handlers know exactly how they will be called. See [Signature Rules](#signature-rules).

```python
from pyeventic import event

# Define an event using a function signature
@event
def on_config_changed(key: str, value: str, /) -> None: ...

# Subscribe a handler to the event
@on_config_changed.subscribe
def log(key: str, value: str) -> None:
    print(f"[Config] {key} was updated to: {value}")

# Trigger the event (using .invoke() or ())
on_config_changed("theme", "dark-mode")

# Output:
# [Config] theme was updated to: dark-mode
```

### Asynchronous Tasks

Eventic has the ability to mix both sync and async handlers. You can await an event to ensure all async tasks finish, or "fire" it to let them run in the background without blocking the main logic.

#### Blocking tasks with `.invoke()` or `()`

```python
import asyncio
from pyeventic import event

# Define an async event using a function signature
@event
async def on_user_signup(user_id: int, /) -> None: ...

# Subscribe a sync handler
@on_user_signup.subscribe
def update_local_cache(user_id: int):
    print(f"User {user_id} added to local cache.")

# Subscribe an async handler
@on_user_signup.subscribe
async def provision_storage(user_id: int):
    await asyncio.sleep(1) # Simulate API call
    print(f"Storage ready for {user_id}!")

async def main():
    # invoke awaits all async handlers before continuing
    await on_user_signup.invoke(42)
    print("Signup flow complete.")

asyncio.run(main())

# Output:
# User 42 added to local cache.
# Storage ready for 42!
# Signup flow complete.
```

#### Non-blocking tasks with `.fire()`

Use `.fire()` for "Fire and Forget" scenarios, like telemetry or logging, where you don't want to make the user wait for a task to complete.

```python
import asyncio
from pyeventic import event

# Define an async event using a function signature
@event
async def on_video_play(video_id: str, /) -> None: ...

@on_video_play.subscribe
async def upload_telemetry(video_id: str):
    await asyncio.sleep(2) # Simulate slow network
    print(f"Telemetry: Analytics for {video_id} uploaded.")

async def main():
    print("User clicked play.")
    
    # fire() schedules the async work but doesn't block the UI
    on_video_play.fire("vid_001")
    
    print("Video started! (UI is not blocked)")
    
    # Optionally wait for background tasks before closing the app
    await on_video_play.wait()
    print("All background tasks finished.")

asyncio.run(main())

# Output:
# User clicked play.
# Video started! (UI is not blocked)
# Telemetry: Analytics for vid_001 uploaded.
# All background tasks finished.
```

### Managing Subscriptions

Eventic provides several ways to manage the lifecycle of a subscription beyond regular subscriptions.

#### Once

With `.once()`, handlers will run exactly once and then automatically unsubscribe.

```python
from pyeventic import Event

class Database:
    def __init__(self):
		# Define a sync event with type hinting
        self.on_connected = Event[[str], None]()
    
    def connect(self) -> None:
        print("Connecting to database...")
		# Invoke the event
        self.on_connected("v1.4.2")

db = Database()

# Subscribe to the event using .once()
@db.on_connected.once
def run_initial_migration(version: str) -> None:
    print(f"Running initial migrations for database version {version}...")

db.connect()
db.connect()

# Output:
# Connecting to database...
# Running initial migrations for database version v1.4.2...
# Connecting to database...
```

#### Context Manager

The context manager provides scoped subscriptions. Handlers will subscribe when the `with` block is entered, and unsubscribe when it is exited.

```python
from pyeventic import Event, event

class Button:
	# Define an event with a method signature
    @event(method=True)
    def on_click(self, x: int, y: int, /) -> None: ...

    def click(self, x: int, y: int) -> None:
		# Invoke the event
        self.on_click(x, y)

button = Button()

# The handler is only subscribed within this block
with button.on_click.subscribed(lambda x, y: print(f"handler: Clicked at ({x}, {y})")):
    button.click(10, 20)

button.click(30, 40)

# Output:
# handler: Clicked at (10, 20)
```

### Events within Classes

`Event` can be used as a Descriptor, meaning it can define events at the class level and will automatically handle creating unique events for each object instance.

```python
from pyeventic import Event

class Battery:
    # Defining an event on the class, but will be unique for every instance of Battery
    on_low_battery = Event[[int], None]()

    def on_power_off(self, percentage: int):
        if percentage <= 5:
            print("Powering off due to low battery.")

    def __init__(self):
        self.percentage = 100
        # Subscribe instance method to its own event
        self.on_low_battery += self.on_power_off

    def drain(self, amount: int):
        self.percentage -= amount
        if self.percentage <= 20:
            # Invoke its own event
            self.on_low_battery.invoke(self.percentage)

laptop = Battery()
phone = Battery() # phone and laptop have independent events
phone.on_low_battery += lambda p: print(f"Low battery: {p}%!")

phone.drain(85)
phone.drain(10)

# Output:
# Low battery: 15%!
# Powering off due to low battery.
# Low battery: 5%!
```

### Subscribe Hooks

Sometimes a system needs to perform work only when something is actually listening (e.g., opening a websocket). `on_subscribe` and `on_unsubscribe` can be used to monitor the events listener count.

```python
from pyeventic import Event

class GameManager:
    def __init__(self) -> None:
        # Define an event for when a player joins the game
        self.on_player_join = Event[[str], None]()

        # Only start listening when someone actually subscribes
        self.on_player_join.on_subscribe.subscribe(self.start_listening)

        # Stop listening when there are no more subscribers
        self.on_player_join.on_unsubscribe.subscribe(self.stop_listening)

    def start_listening(self, event, callable) -> None:
        # If the length of event is 1, it means this is the first subscriber
        if len(event) == 1:
            print(f"Started listening for player_join notifications from the server.")

    def stop_listening(self, event, callable) -> None:
        # If the length of event is 0, it means there are no more subscribers
        if len(event) == 0:
            print(f"Stopped listening for player_join notifications from the server.")

    def join(self, player_name: str) -> None:
        self.on_player_join(player_name)

game_manager = GameManager()

func = lambda name: print(f"Player {name} has joined the game!")
game_manager.on_player_join += func

game_manager.join("Alice")

game_manager.on_player_join -= func

# Output:
# Started listening for player_join notifications from the server.
# Player Alice has joined the game!
# Stopped listening for player_join notifications from the server.
```

### Event Options

Events accept one option, `on_error` (see [Handling Exceptions](#handling-exceptions)). Decorated methods also need `method=True`.

```python
from pyeventic import Event, event

# Decorating a function
@event(on_error=print)
def on_save(path: str, /) -> None: ...

# Decorating a method
class Document:
    @event(method=True, on_error=print)
    def on_close(self, *, discard_changes: bool) -> None: ...

# Without a decorator
def on_load(path: str, /) -> None: ...
loaded = event(on_load, on_error=print)

# Without a signature function
progress = Event[[int], None](on_error=print)
```

> [!NOTE]
> Use `@event(method=True)` on methods to remove `self` / `cls` from the event signature. With plain `@event`, `self` stays in the signature and is passed when the event is invoked.

### Signature Rules

An event's signature is a contract with every handler. If a parameter can be passed either by position or by name, a handler can't know which one the event will use, so a handler that renames the parameter, or only accepts it one way, may break. Eventic checks the signature when the event is defined:

```python
from pyeventic import event

@event
def on_move(x: int, y: int) -> None: ...
# TypeError: Event parameter 'x' must be positional-only or keyword-only. Add '/' or '*' to the signature.

@event
def on_move(x: int, y: int, /) -> None: ...         # OK: handlers are called as handler(x, y)

@event
def on_resize(*, width: int, height: int) -> None: ...  # OK: handlers are called as handler(width=..., height=...)

@event
def on_scroll(amount: int = 1, /) -> None: ...
# TypeError: Event parameter 'amount' cannot have a default value.

@event
def on_anything(*args: int) -> None: ...
# TypeError: Event parameter 'args' cannot be *args or **kwargs.
```

Default values are not allowed, since it would be unclear whether handlers receive the argument. `*args` and `**kwargs` are not allowed either, since handlers couldn't know what they will receive. To define an event without a signature function, use `Event[[int], None]()`; its signature is then only checked by the type checker.

These rules only apply to the event's signature. Handlers are free to accept arguments however they like, as long as the type checker accepts them, for example with extra parameters that have defaults.

### Handling Exceptions

Handlers are responsible for their own exceptions. If a handler raises, the exception is ignored and the remaining handlers still run. To see these exceptions, pass `on_error`, which is called with each one:

```python
from pyeventic import event

def report(exc: Exception) -> None:
    print(f"A handler failed: {exc!r}")

@event(on_error=report)
def on_shutdown() -> None: ...

@on_shutdown.subscribe
def close_database() -> None:
    raise ConnectionError("Database already closed")

@on_shutdown.subscribe
def flush_logs() -> None:
    print("Logs flushed.")

on_shutdown()

# Output:
# A handler failed: ConnectionError('Database already closed')
# Logs flushed.
```

> [!NOTE]
> * For synchronous handlers, `on_error` is called during `invoke()`. For asynchronous handlers, it is called once they have all finished, when the returned coroutine is awaited (or the `Task` returned by `fire()` finishes).
> * If `on_error` itself raises, that exception propagates: from `invoke()` for synchronous handlers (the remaining handlers are not called), or from the awaited coroutine (or the `Task` from `fire()`) for asynchronous handlers.
