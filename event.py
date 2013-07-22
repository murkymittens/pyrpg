class Event(object):
	TYPE_OUTPUT = 0

	def __init__(self, type):
		self.type = type

	def setData(self, data):
		self.data = data

	def getData(self):
		return self.data

class EventListener(object):
	def __init__(self):
		self.events = []

	