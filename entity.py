class Entity:
	def __init__(self, name = "Generic Entity", health = 10, attack = 1, defense = 0):
		self.name = name
		self.health = health
		self.attack = attack
		self.defense = defense

	def isAlive(self):
		return self.health > 0

	def setHealth(self, health):
		self.health = health

	def getHealth(self):
		return self.health

	def setAttack(self, attack):
		self.attack = attack

	def getAttack(self):
		return self.attack

	def setDefense(self, defense):
		self.defense = defense

	def getDefense(self):
		return self.defense