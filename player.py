from entity import Entity

class Player(Entity):
	STATE_EXPLORING = 0
	STATE_BATTLE = 1
	EXPERIENCE_TARGET = 100

	def __init__(self, name, health = 10, attack = 1, defense = 0):
		Entity.__init__(self, name, health, attack, defense)
		self.state = Player.STATE_EXPLORING

	def setState(self, state):
		self.state = state

	def getState(self):
		return self.state

	def levelUp(self):
		levels = self.experience / Player.EXPERIENCE_TARGET
		remaining_experience = self.experience - levels * Player.EXPERIENCE_TARGET
		healthScaling = 12
		attackScaling = 2
		defenseScaling = 1
		self.health = self.health + levels * healthScaling
		self.attack = self.attack + levels * attackScaling
		self.defense = self.defense + levels * defenseScaling
		self.experience = remaining_experience
