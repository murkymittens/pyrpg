from entity import Entity
from player import Player
from world import World
from random import randint

def chanceRoll(probability):
	chance_roll = randint(1, 100)
	return chance_roll <= probability

def sayHp(entity):
	print "%s has %d/%d HP." % (entity.name, entity.getHealth(), entity.getMaximumHealth())

def attack(attacker, defender):
	if chanceRoll(75):
		attack_value = attacker.getAttack()
		if chanceRoll(50):
			attack_value -= defender.getDefense()
			if attack_value < 0:
				attack_value = 0
		defender.setHealth(defender.getHealth() - attack_value)
		print "%s hits %s for %d." % (attacker.name, defender.name, attack_value)
		sayHp(defender)
	else:
		print "%s misses." % (attacker.name)

name = raw_input("What is your name? ")
player = Player(name)
world = World(player)
lastCommand = None
skipInput = False

while player.isAlive():
	if not skipInput:
		command = raw_input("What do you want to do? ")
		skipInput = True

	if len(command) == 0 and lastCommand != None:
		command = lastCommand

	if command == "explore" or command == "e":
		if player.getState() == Player.STATE_EXPLORING:
			world.setStepsTaken(world.getStepsTaken() + 1)
			if chanceRoll(10):
				world.generateMonster()
				enemy = world.getEnemy()
				player.setState(Player.STATE_BATTLE)
				print "You've encountered a %s. Prepare to fight." % (world.getEnemy().name)
				skipInput = False
			elif chanceRoll(20):
				player.setHealthPotions(player.getHealthPotions() + 1)
				print "You found a health potion! You now have %d health potions." % (player.getHealthPotions())
				skipInput = False
			elif chanceRoll(5):
				player.setHealth(player.getHealth() * 0.25)
				if player.getHealth() < 1:
					player.setHealth(1)
				print "You were careless and fell into a hole."
				sayHp(player)
				skipInput = False
			else:
				if player.getHealth() < player.getMaximumHealth():
					player.setHealth(player.getHealth() + 1)
					print "You've recovered 1 HP."
					sayHp(player)
				player.setExperience(player.getExperience() + 1)
				print "You've received 1 EXP."
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
				if(player.getExperience() >= Player.EXPERIENCE_TARGET):
					player.levelUp()
					print "%s has leveled up!" % (player.name)
				sayHp(player)
		else:
			print "You can't do that right now."
		skipInput = False
	elif command == "health" or command == "h":
		if player.getHealthPotions() > 0:
			player.setHealth(player.getHealth() + 10)
			player.setHealthPotions(player.getHealthPotions() - 1)
			print "You've been healed for 10 HP. You have %d health potions left." % (player.getHealthPotions())
			sayHp(player)
		else:
			print "You don't have any more health potions."
		skipInput = False
	elif command == "exit" or command == "x":
		break
	else:
		print "I don't understand you."
		skipInput = False

	lastCommand = command
	if not skipInput:
		print ''

print "You have died. Your princess is in a different castle. Your life sucks...or it would, if you had one!"
