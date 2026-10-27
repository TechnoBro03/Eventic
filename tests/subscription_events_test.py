from typing import Awaitable, Callable
from pyeventic import Event

def test_subscription_events():
	event = Event[[], None]()
	sub_log: list[Callable[[], None | Awaitable[None]]] = []
	unsub_log: list[Callable[[], None | Awaitable[None]]] = []
	
	event.on_subscribe.subscribe(lambda e, h: sub_log.append(h))
	event.on_unsubscribe.subscribe(lambda e, h: unsub_log.append(h))
	
	def h(): pass
	event.subscribe(h)
	event.unsubscribe(h)
	
	assert sub_log == [h]
	assert unsub_log == [h]

def test_subscription_readonly():
	event = Event[[], None]()
	sub = event.on_subscribe
	unsub = event.on_unsubscribe
	
	event.on_subscribe = Event()
	event.on_unsubscribe = Event()

	assert event.on_subscribe is sub
	assert event.on_unsubscribe is unsub
