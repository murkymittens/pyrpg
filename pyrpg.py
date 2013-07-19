from entity import Entity
from player import Player
from world import World
from random import randint
from time import sleep

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

print ''
print "Welcome to the most evil dungeon you will ever face %s!" % (player.name)
print "Please use 'e' to explore, 'a' to attack, 'b' to buy potions, and 'h' to heal."
print "Should you find this dungeon too...hard, feel free to 'x' to commit suicide and end your eternal damnation on earth \
and begin your eternal damnation in hell. *cackle*"
print ''

while player.isAlive():
	if not skipInput:
		rawCommand = raw_input("What do you want to do? ")
		splitCommand = rawCommand.split(' ', 1)
		command = splitCommand[0]
		skipInput = True

	if len(command) == 0 and lastCommand != None:
		command = lastCommand

	if command == "explore" or command == "e":
		if player.getState() == Player.STATE_SHOPPING:
			player.setState(Player.STATE_EXPLORING)

		if player.getState() == Player.STATE_EXPLORING:
			world.setStepsTaken(world.getStepsTaken() + 1)
			if player.getHealth() < player.getMaximumHealth():
				player.setHealth(player.getHealth() + 1)
				print "You've recovered 1 HP."
				sayHp(player)
			player.setExperience(player.getExperience() + 1)
			print "You've received 1 EXP."

			if chanceRoll(10):
				world.generateMonster()
				enemy = world.getEnemy()
				player.setState(Player.STATE_BATTLE)
				print "You've encountered a %s. Prepare to fight." % (world.getEnemy().name)
				skipInput = False
			elif chanceRoll(20):
				player.setHealthPotions(player.getHealthPotions() + 1)
				print "You found a health potion! You now have %d health potions." % (player.getHealthPotions())
			elif chanceRoll(10):
				gain = randint(5, 50)
				rewardTypeRoll = randint(1, 100)
				print "%s found an ancient artifact." % (player.name)
				if rewardTypeRoll <= 50:
					player.setExperience(player.getExperience() + gain)
					print "%s got %d EXP." % (player.name, gain)
				else:
					player.setGold(player.getGold() + gain)
					print "%s got %d gold." % (player.name, gain)
			elif chanceRoll(10):
				player.setState(Player.STATE_SHOPPING)
				print "%s stumbled into a rickety shack. There appear to be items for sale. You have %d gold." % (player.name, player.getGold())
				skipInput = False
			elif chanceRoll(5):
				player.setHealth(player.getHealth() * 0.25)
				if player.getHealth() < 1:
					player.setHealth(1)
				print "You were careless and fell into a hole."
				sayHp(player)
			elif chanceRoll(5):
				somethingStolen = False
				if player.getGold() > 0:
					somethingStolen = True
					player.setGold(player.getGold() * 0.5)
				
				if player.getHealthPotions() > 0:
					somethingStolen = True
					player.setHealthPotions(player.getHealthPotions() * 0.5)

				if somethingStolen:
					print ("%s's pockets feel lighter. You feel around. You have %d gold and %d health potions. Something's definitely missing..." % 
						(player.name, player.getGold(), player.getHealthPotions()))
		else:
			print "You can't do that right now."
			skipInput = False
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
				player.setGold(player.getGold() + enemy.getGold())
				print "%s got %d EXP and %d gold." % (player.name, enemy.getExperience(), enemy.getGold())
				sayHp(player)
				enemy = None
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

	elif command == "buy" or command == "b":
		if player.getState() == Player.STATE_SHOPPING:
			healthPotionCost = 5
			if len(splitCommand) > 1:
				quantity = int(splitCommand[1])
			else:
				quantity = 1

			purchaseCost = healthPotionCost * quantity
			if player.getGold() >= purchaseCost:
				player.setGold(player.getGold() - purchaseCost)
				player.setHealthPotions(player.getHealthPotions() + quantity)
				print "%s bought (%d) health potion for %d gold. You now have %d health potions. You have %d gold." % (player.name, quantity, purchaseCost, 
					player.getHealthPotions(), player.getGold())
			else:
				print "The frail-looking shopkeeper banishes you from the premises with unusual vigor, shouting \"My potions cost %d gold! Begone!\"." % (healthPotionCost)
		else:
			print "You can't shop right now."
		skipInput = False
	elif command == "exit" or command == "x":
		break
	else:
		print "I don't understand you."
		skipInput = False

	if(player.getExperience() >= Player.EXPERIENCE_TARGET):
		player.levelUp()
		print "%s has leveled up to %d!" % (player.name, player.getLevel())
		sayHp(player)

	lastCommand = command
	if not skipInput:
		print ''
	sleep(0.5)

print "You have died. Your princess is in a different castle. Your life sucks...or it would, if you had one!"
print "%s was level %d with %d health potions, %d/%d EXP, and %d gold." % (player.name, player.getLevel(), player.getHealthPotions(),
	player.getExperience(), Player.EXPERIENCE_TARGET, player.getGold())
if enemy != None:
	print "%s was killed by %s." % (player.name, enemy.name)
