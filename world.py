from entity import Entity
import random

class World:
	MONSTER_NAMES = "Goblin", "Imp", "Orc", "Grue"
	MONSTER_CLASSES = "Frail", "Common", "Brawny", "Elite", "Legendary"

	def __init__(self, player):
		self.player = player
		self.stepsTaken = 0
		self.enemy = None

	def generateMonster(self):
		healthScaling = 0.75
		attackScaling = 0.25
		defenseScaling = 0.25
		modifier = self.stepsTaken / 10
		if modifier >= len(World.MONSTER_CLASSES):
			monsterClass = len(World.MONSTER_CLASSES) - 1
		else:
			monsterClass = modifier
		monsterName = random.choice(World.MONSTER_NAMES)
		self.enemy = Entity(World.MONSTER_CLASSES[monsterClass] + " " + monsterName, 
			10 + healthScaling * modifier, 1 + attackScaling * modifier, 0 + defenseScaling * modifier)

	def setEnemy(self, enemy):
		self.enemy = enemy

	def getEnemy(self):
		return self.enemy

	def setStepsTaken(self, stepsTaken):
		self.stepsTaken = stepsTaken

	def getStepsTaken(self):
		return self.stepsTaken