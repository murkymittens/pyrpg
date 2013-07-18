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
		healthScaling = 10
		attackScaling = 1
		defenseScaling = 0.5
		modifier = self.stepsTaken / 50
		if modifier >= len(World.MONSTER_CLASSES):
			monsterClass = World.MONSTER_CLASSES[len(World.MONSTER_CLASSES) - 1]
		else:
			monsterClass = World.MONSTER_CLASSES[modifier]
		monsterName = random.choice(World.MONSTER_NAMES)
		self.enemy = Entity(monsterClass + " " + monsterName, 
			10 + int(healthScaling * modifier), 1 + int(attackScaling * modifier), 0 + int(defenseScaling * modifier))
		self.enemy.setExperience(self.enemy.getHealth())

	def setEnemy(self, enemy):
		self.enemy = enemy

	def getEnemy(self):
		return self.enemy

	def setStepsTaken(self, stepsTaken):
		self.stepsTaken = stepsTaken

	def getStepsTaken(self):
		return self.stepsTaken