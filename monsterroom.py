from room import Room
from random import choice
from entity import Entity
from util import happens

class MonsterRoom(Room):
	MONSTER_NAMES = "Goblin", "Imp", "Orc", "Grue", "Merman", "Ratman", "Lizardman", "Slime", "Bandit", "Assassin"
	MONSTER_CLASSES = "Frail", "Lesser", "Common", "Greater", "Brawny", "Elite", "Legendary"
	HEALTH_SCALING = 10
	ATTACK_SCALING = 1
	DEFENSE_SCALING = 0.5
	GOLD_SCALING = 2
	BOSS_HEALTH_SCALING = 10
	BOSS_ATTACK_SCALING = 4
	BOSS_DEFENSE_SCALING = 1.5
	BOSS_GOLD_SCALING = 10
	BOSS_EXPERIENCE_SCALING = 10

	def __init__(self, stepsTaken, monstersEncountered):
		super(MonsterRoom, self).__init__(Room.TYPE_MONSTER)
		monsterModifier = int(stepsTaken / 50)
		monsterName = choice(MonsterRoom.MONSTER_NAMES)
		if monsterModifier > len(MonsterRoom.MONSTER_CLASSES):
			monsterClass = MonsterRoom.MONSTER_CLASSES[len(MonsterRoom.MONSTER_CLASSES) - 1]
		else:
			monsterClass = MonsterRoom.MONSTER_CLASSES[monsterModifier]
		monster = Entity()
		monster.name = monsterClass + " " + monsterName
		monster.setMaximumHealth(10 + MonsterRoom.HEALTH_SCALING * monsterModifier)
		monster.setHealth(monster.getMaximumHealth())
		monster.setAttack(1 + MonsterRoom.ATTACK_SCALING * monsterModifier)
		monster.setDefense(0 + MonsterRoom.DEFENSE_SCALING * monsterModifier)
		monster.setExperience(monster.getHealth())
		monster.setGold(1 + MonsterRoom.GOLD_SCALING * monsterModifier)

		if monstersEncountered > 10:
			if happens(10):
				monster.name = "Boss " + monster.name
				monster.setMaximumHealth(monster.getMaximumHealth() * MonsterRoom.BOSS_HEALTH_SCALING)
				monster.setHealth(monster.getMaximumHealth())
				monster.setAttack(monster.getAttack() * MonsterRoom.BOSS_ATTACK_SCALING)
				monster.setDefense(monster.getDefense() * MonsterRoom.BOSS_DEFENSE_SCALING)
				monster.setExperience(monster.getExperience() * MonsterRoom.BOSS_EXPERIENCE_SCALING)
				monster.setGold(monster.getGold() * MonsterRoom.BOSS_GOLD_SCALING)

		self.enemy = monster

		print "You've encountered a {monster}. Prepare to fight.".format(monster=monster.name)

	def interact(self, player, command):
		if command == "attack" or command == "a":
			player.attackTarget(self.enemy)
			if self.enemy.isAlive():
				self.enemy.attackTarget(player)
			else:
				print "{player} has vanquished {monster}.".format(player=player.name, monster=self.enemy.name)
				print "Received {gold} gold and {exp} EXP.".format(gold=self.enemy.getGold(), exp=self.enemy.getExperience())
				player.setHealth(player.getHealth() + 10)
				player.setExperience(player.getExperience() + self.enemy.getExperience())
				player.setGold(player.getGold() + self.enemy.getGold())
				player.announceHealth()
				self.enemy = None
				player.shieldBubble.active = False
			player.shieldBubble.update()
			return True

		elif command == "health" or command == "h":
			if player.getHealthPotions() > 0:
				player.setHealth(player.getHealth() + 10)
				player.setHealthPotions(player.getHealthPotions() - 1)
				print "You've been healed for 10 HP. You have {pots} health potions left.".format(pots=player.getHealthPotions())
				player.announceHealth()
			else:
				print "You don't have any more health potions."
			return True

		elif command == "shieldbubble" or command == "sb":
			if player.shieldBubble.cooldown == 0:
				player.shieldBubble.activate()
				print "{player} has activated Shield Bubble.".format(player=player.name)
			else:
				print "Shield Bubble is still on cooldown. {turns} turns left.".format(turns=player.shieldBubble.cooldown)
			return True
			
		elif command == "negotiate" or command == "n":
			if player.getGold() > 0:
				player.setGold(player.getGold() * 0.5)
				print "{player} throws some gold in the general direction of {monster} and tries to duck out of sight.".format(player=player.name,
					monster=self.enemy.name)
				if happens(50):
					print "{monster}, momentarily distracted by shiny gold coins, loses track of {player} and wanders off.".format(monster=self.enemy.name,
						player=player.name)
					self.enemy = None
				else:
					print "The gold coins bounce off {monster}'s body and clink to the ground. {monster} seems unimpressed.".format(monster=self.enemy.name)
			else:
				print "Sadly, {player} has no gold to negotiate with...".format(player=player.name)
			return True

		else:
			return False

	def isPassable(self):
		return self.enemy == None