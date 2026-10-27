from pyeventic import Event

def test_invoke_sync():
	event = Event[[], None]()
	results: list[int] = []
	
	def h1(): results.append(1)
	def h2(): results.append(2)
	
	event.subscribe(h1)
	event.subscribe(h2)
	
	# invoke() custom _Awaitable (empty for sync handlers)
	event.invoke()
	assert set(results) == {1, 2}

def test_invoke_exception_ignored():
	event = Event[[], None]()
	results: list[int] = []

	def h1(): results.append(1)
	def h2(): raise ValueError("Handler error")
	def h3(): results.append(3)

	event.subscribe(h1)
	event.subscribe(h2)
	event.subscribe(h3)

	# Without on_error, the exception is ignored and the remaining handlers are still called
	event.invoke()
	assert results == [1, 3]

def test_call_sync():
	event = Event[[], None]()
	called = False
	
	def h(): nonlocal called; called = True
	event.subscribe(h)
	
	event()
	assert called is True
