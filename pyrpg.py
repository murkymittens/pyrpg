from entity import Entity
from player import Player
from world import World
from random import randint

def chanceRoll(probability):
	chance_roll = randint(1, 100)
	return chance_roll <= probability

def attack(attacker, defender):
	if chanceRoll(75):
		attack_value = attacker.getAttack()
		if chanceRoll(50):
			attack_value -= defender.getDefense()
			if attack_value < 0:
				attack_value = 0
		defender.setHealth(defender.getHealth() - attack_value)
		print "%s hits %s for %d. %s's health is now %d." % (attacker.name, defender.name, attack_value, defender.name, defender.getHealth())
	else:
		print "%s misses." % (attacker.name)

name = raw_input("What is your name? ")
player = Player(name)
world = World(player)

while player.isAlive():
	command = raw_input("What do you want to do? ")
	if command == "explore" or command == "e":
		if player.getState() == Player.STATE_EXPLORING:
			world.setStepsTaken(world.getStepsTaken() + 1)
			if chanceRoll(10):
				world.generateMonster()
				enemy = world.getEnemy()
				player.setState(Player.STATE_BATTLE)
				print "You've encountered a %s. Prepare to fight." % (world.getEnemy().name)
			elif chanceRoll(20):
				player.setHealthPotions(player.getHealthPotions + 1)
				print "You found a health potion! You now have %d health potions." % (player.getHealthPotions())
			else:
				player.setHealth(player.getHealth() + 1)
				print "You've recovered 1 HP. Your HP is now %d." % (player.getHealth())
		else:
			print "You can't do that right now."
	elif command == "attack" or command == "a":
		if player.getState() == Player.STATE_BATTLE:
			enemy = world.getEnemy()
			attack(player, enemy)
			if enemy.isAlive():
				attack(enemy, player)
			else:
				world.setEnemy(None)
				player.setState(Player.STATE_EXPLORING)
				print "%s has vanquished the %s. Prepare your anus for the spoils of victory!" % (player.name, enemy.name)
				player.setHealth(player.getHealth() + 10)
				player.setExperience(player.getExperience() + enemy.getExperience())
				print "%s got %d EXP." % (player.name, enemy.getExperience())
				print "%s's HP is now %d." % (player.name, player.getHealth())
				if(player.getExperience() >= Player.EXPERIENCE_TARGET):
					player.levelUp()
					print "%s has leveled up!" % (player.name)
		else:
			print "You can't do that right now."
	elif command == "health" or command == "h":
		if player.getHealthPotions() > 0:
			player.setHealth(player.getHealth() + 10)
			player.setHealthPotions(player.getHealthPotions() - 1)
			print "You've been healed for 10 HP. Your HP is now %d. You have %d health potions left." % (player.getHealth(), player.getHealthPotions())
		else:
			print "You don't have any more health potions."
	elif command == "exit" or command == "x":
		break
	else:
		print "I don't understand you."
	print ''

print "You have died. Your princess is in a different castle. Your life sucks...or it would, if you had one!"
