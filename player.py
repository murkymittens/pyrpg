from entity import Entity

class Player(Entity):
	STATE_EXPLORING = 0
	STATE_BATTLE = 1
	EXPERIENCE_TARGET = 100

	def __init__(self, name, health = 10, attack = 1, defense = 0):
		Entity.__init__(self, name, health, attack, defense)
		self.state = Player.STATE_EXPLORING
		self.healthPotions = 1
		self.level = 1

	def setState(self, state):
		self.state = state

	def getState(self):
		return self.state

	def levelUp(self):
		levels = self.experience / Player.EXPERIENCE_TARGET
		remaining_experience = self.experience - levels * Player.EXPERIENCE_TARGET
		healthScaling = 10
		attackScaling = 1
		defenseScaling = 0.5
		self.maximumHealth = self.maximumHealth + int(levels * healthScaling)
		self.health = self.maximumHealth
		self.attack = self.attack + int(levels * attackScaling)
		self.defense = self.defense + int(levels * defenseScaling)
		self.experience = remaining_experience
		Player.EXPERIENCE_TARGET = int(Player.EXPERIENCE_TARGET * 1.25)
		self.level = self.level + 1

	def setHealthPotions(self, healthPotions):
		self.healthPotions = healthPotions

	def getHealthPotions(self):
		return self.healthPotions

	def setLevel(self, level):
		self.level = level

	def getLevel(self):
		return self.level
