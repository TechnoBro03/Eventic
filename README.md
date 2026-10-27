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

## Features
* **Type Safety**: Strongly typed, fully compatible with many type checkers, with autocomplete for event signatures.
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
| [event()](docs/event.md) | Method | Create an Event from a instance or class method. |

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

```python
from pyeventic import Event

# Define an event using a function signature
@Event
def on_config_changed(key: str, value: str) -> None: ...

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
from pyeventic import Event

# Define an async event using a function signature
@Event
async def on_user_signup(user_id: int) -> None: ...

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
from pyeventic import Event

# Define an async event using a function signature
@Event
async def on_video_play(video_id: str) -> None: ...

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
    @event
    def on_click(self, x: int, y: int) -> None: ...

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