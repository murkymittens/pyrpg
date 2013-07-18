class Entity:
	def __init__(self, name = "Generic Entity", health = 10, attack = 1, defense = 0):
		self.name = name
		self.health = health
		self.attack = attack
		self.defense = defense
		self.experience = 0

	def isAlive(self):
		return int(self.health) > 0

	def setHealth(self, health):
		self.health = int(health)

	def getHealth(self):
		return self.health

	def setAttack(self, attack):
		self.attack = int(attack)

	def getAttack(self):
		return self.attack

	def setDefense(self, defense):
		self.defense = int(defense)

	def getDefense(self):
		return self.defense

	def setExperience(self, experience):
		self.experience = int(experience)

	def getExperience(self):
		return self.experience