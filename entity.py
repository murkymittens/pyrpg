from skill import SimpleBuff
from util import happens

class Entity:
	def __init__(self, name = "Generic Entity", health = 10, attack = 1, defense = 0):
		self.name = name
		self.health = health
		self.maximumHealth = health
		self.attack = attack
		self.defense = defense
		self.experience = 0
		self.gold = 0
		self.hitRate = 75
		self.shieldBubble = SimpleBuff("Shield Bubble", 5, 8)

	def attackTarget(self, target):
		if happens(self.hitRate):
			attackValue = self.attack
			if target.shieldBubble.active:
				attackValue = 0
				print "{name}'s Shield Bubble absorbs all damage.".format(name=target.name)
			elif happens(50):
				attackValue = attackValue - target.getDefense()
			if attackValue < 0:
				attackValue = 0
			target.setHealth(target.getHealth() - attackValue)
			print "{attacker} hit {defender} for {damage} damage.".format(attacker=self.name, defender=target.name, damage=attackValue)
			target.announceHealth()
		else:
			print "{name} misses.".format(name=self.name)

	def announceHealth(self):
		print "{name} has {hp}/{maxhp}.".format(name=self.name, hp=self.health, maxhp=self.maximumHealth)

	def isAlive(self):
		return int(self.health) > 0

	def setHealth(self, health):
		self.health = int(health)
		if self.health > self.maximumHealth:
			self.health = self.maximumHealth
		elif self.health < 0:
			self.health = 0

	def getHealth(self):
		return self.health

	def setMaximumHealth(self, health):
		self.maximumHealth = int(health)

	def getMaximumHealth(self):
		return self.maximumHealth

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

	def setGold(self, gold):
		self.gold = int(gold)
		if self.gold < 0:
			self.gold = 0

	def getGold(self):
		return self.gold

	def setHitRate(self, hitRate):
		self.hitRate = hitRate

	def getHitRate(self):
		return self.hitRate