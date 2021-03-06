from entity import Entity

class Player(Entity):
	STATE_EXPLORING = 0
	STATE_BATTLE = 1
	STATE_SHOPPING = 2

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
		healthScaling = 3.5
		attackScaling = 0.6
		defenseScaling = 0.25
		self.maximumHealth = self.maximumHealth + int(self.level * healthScaling)
		self.health = self.maximumHealth
		self.attack = self.attack + int(self.level * attackScaling)
		self.defense = self.defense + int(self.level * defenseScaling)
		self.experience = remaining_experience
		Player.EXPERIENCE_TARGET = int(Player.EXPERIENCE_TARGET * 1.25)
		self.level = self.level + levels

	def setHealthPotions(self, healthPotions):
		self.healthPotions = int(healthPotions)
		if self.healthPotions < 0:
			self.healthPotions = 0

	def getHealthPotions(self):
		return self.healthPotions

	def setLevel(self, level):
		self.level = level

	def getLevel(self):
		return self.level
