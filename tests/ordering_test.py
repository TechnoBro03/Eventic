from pyeventic import Event

def test_invoke_subscription_order():
	event = Event[[], None]()
	results: list[int] = []

	for i in range(10):
		event.subscribe(lambda i=i: results.append(i)) # type: ignore # Default arg captures the loop value

	event.invoke()
	assert results == list(range(10))

def test_resubscribe_moves_to_end():
	event = Event[[], None]()
	results: list[int] = []
	def h1(): results.append(1)
	def h2(): results.append(2)

	event += h1
	event += h2
	event -= h1
	event += h1

	event.invoke()
	assert results == [2, 1]
