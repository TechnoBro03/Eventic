from pyeventic import Event

class Owner:
	evt = Event[[], None]()

def test_descriptor_instance_creation():
	o1 = Owner()
	o2 = Owner()
	# Accessing from instances should create separate Event objects
	assert o1.evt is not o2.evt
	assert o1.evt is not Owner.evt
	assert o1.evt._owner is Owner # type: ignore # _owner is private
	assert o1.evt._name == "evt" # type: ignore # _name is private

def test_descriptor_set_prevention():
	o = Owner()
	original_evt = o.evt
	o.evt = Event[[], None]() # Should be ignored by __set__
	assert o.evt is original_evt

def test_descriptor_instance_cached():
	o = Owner()
	assert o.evt is o.evt
