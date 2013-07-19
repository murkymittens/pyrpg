from entity import Entity
from random import randint
import random

class World:
	MONSTER_NAMES = "Goblin", "Imp", "Orc", "Grue"
	MONSTER_CLASSES = "Frail", "Common", "Brawny", "Elite", "Legendary"

	def __init__(self, player):
		self.player = player
		self.stepsTaken = 0
		self.enemy = None
		self.bossSafePeriod = 10

	def generateMonster(self):
		self.bossSafePeriod = self.bossSafePeriod - 1
		boss = False
		if self.bossSafePeriod < 0:
			bossRoll = randint(1, 100)
			if bossRoll <= 10:
				boss = True

		healthScaling = 10
		attackScaling = 1
		defenseScaling = 0.5
		goldScaling = 2
		modifier = self.stepsTaken / 50
		if boss:
			monsterClass = "Boss"
		else:
			if modifier >= len(World.MONSTER_CLASSES):
				monsterClass = World.MONSTER_CLASSES[len(World.MONSTER_CLASSES) - 1]
			else:
				monsterClass = World.MONSTER_CLASSES[modifier]

		monsterName = random.choice(World.MONSTER_NAMES)
		self.enemy = Entity(monsterClass + " " + monsterName, 
			10 + int(healthScaling * modifier), 1 + int(attackScaling * modifier), 0 + int(defenseScaling * modifier))
		self.enemy.setExperience(self.enemy.getHealth())
		self.enemy.setGold(1 + int(goldScaling * modifier))
		if boss:
			self.enemy.setMaximumHealth(self.enemy.getMaximumHealth() * 10)
			self.enemy.setHealth(self.enemy.getMaximumHealth())
			self.enemy.setAttack(self.enemy.getAttack() * 2.5)
			self.enemy.setDefense(self.enemy.getDefense() * 1.1)
			self.enemy.setGold(self.enemy.getGold() * 10)
			self.enemy.setExperience(self.enemy.getExperience() * 10)

	def setEnemy(self, enemy):
		self.enemy = enemy

	def getEnemy(self):
		return self.enemy

	def setStepsTaken(self, stepsTaken):
		self.stepsTaken = stepsTaken

	def getStepsTaken(self):
		return self.stepsTaken