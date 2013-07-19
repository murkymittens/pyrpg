from random import randint

class ChanceBasedEvent:
	def attempt(self, probability):
		roll = randint(1, 100)
		return roll <= probability