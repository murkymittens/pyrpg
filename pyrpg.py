from player import Player
from world import World
from random import randint
from time import sleep
from util import ChanceBasedEvent

def chanceRoll(probability):
	chance_roll = randint(1, 100)
	return chance_roll <= probability

def sayHp(entity):
	print "%s has %d/%d HP." % (entity.name, entity.getHealth(), entity.getMaximumHealth())

def attack(attacker, defender):
	if chanceRoll(75):
		attack_value = attacker.getAttack()
		if chanceRoll(50):
			attack_value = attack_value - defender.getDefense()
			if attack_value < 0:
				attack_value = 0
		if defender.shieldBubble.active:
			attack_value = 0
			print "%s's Shield Bubble absorbs all damage." % (defender.name)
		defender.setHealth(defender.getHealth() - attack_value)
		print "%s hits %s for %d." % (attacker.name, defender.name, attack_value)
		sayHp(defender)
	else:
		print "%s misses." % (attacker.name)

def printCommands():
	print "Please use 'e' to explore, 'a' to attack, 'b' to buy potions, 'sb' to activate your shield bubble, 'h' to heal, 'n' to negotiate, or 'x' to commit suicide."

name = raw_input("What is your name? ")
player = Player(name)
world = World(player)
lastCommand = None
skipInput = False
enemy = None
chance = ChanceBasedEvent()

print ''
print "Welcome to the most evil dungeon you will ever face %s!" % (player.name)
printCommands()
print "Should you find this dungeon too...hard, feel free to commit suicide and end your eternal damnation on earth \
and begin your eternal damnation in hell. *cackle*"
print ''

while player.isAlive():
	if not skipInput:
		rawCommand = raw_input("What do you want to do? ")
		splitCommand = rawCommand.split(' ', 1)
		command = splitCommand[0]
		# skipInput = True
	else:
		skipInput = False

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
				# skipInput = False
			elif chanceRoll(20):
				skipInput = True
				player.setHealthPotions(player.getHealthPotions() + 1)
				print "You found a health potion! You now have %d health potions." % (player.getHealthPotions())
			elif chanceRoll(10):
				skipInput = True
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
				# skipInput = False
			elif chanceRoll(5):
				skipInput = True
				player.setHealth(player.getHealth() * 0.25)
				if player.getHealth() < 1:
					player.setHealth(1)
				print "You were careless and fell into a hole."
				sayHp(player)
			elif chanceRoll(5):
				skipInput = True
				somethingStolen = False
				if player.getGold() > 0:
					somethingStolen = True
					player.setGold(player.getGold() * 0.5)
				
				if player.getHealthPotions() > 0:
					somethingStolen = True
					player.setHealthPotions(player.getHealthPotions() * 0.75)

				if somethingStolen:
					print ("%s's pockets feel lighter. You feel around. You have %d gold and %d health potions. Something's definitely missing..." % 
						(player.name, player.getGold(), player.getHealthPotions()))
			else:
				skipInput = True
		else:
			print "You can't do that right now."
			# skipInput = False
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
				#player.shieldBubble.reset()
				player.shieldBubble.active = False
			player.shieldBubble.update()

		else:
			print "You can't do that right now."
		# skipInput = False
	elif command == "health" or command == "h":
		if player.getHealthPotions() > 0:
			player.setHealth(player.getHealth() + 10)
			player.setHealthPotions(player.getHealthPotions() - 1)
			print "You've been healed for 10 HP. You have %d health potions left." % (player.getHealthPotions())
			sayHp(player)
		else:
			print "You don't have any more health potions."
		# skipInput = False

	elif command == "buy" or command == "b":
		if player.getState() == Player.STATE_SHOPPING:
			healthPotionCost = 5
			if len(splitCommand) > 1:
				try:
					quantity = int(splitCommand[1])
				except (TypeError, ValueError):
					quantity = 1
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
		# skipInput = False

	elif command == "shieldbubble" or command == "sb":
		if player.getState() == Player.STATE_BATTLE:
			if player.shieldBubble.cooldown == 0:
				player.shieldBubble.activate()
				print "%s has activated Shield Bubble." % (player.name)
			else:
				print "Shield Bubble is still on cooldown. %d turns left." % (player.shieldBubble.cooldown)
		else:
			print "You can't activate your skill outside of battle."
		# skipInput = False

	elif command == "negotiate" or command == "n":
		if player.getState() == Player.STATE_BATTLE:
			if player.getGold() > 0:
				player.setGold(player.getGold() * 0.5)
				print "%s throws some gold in the general direction of %s and tries to duck out of sight." % (player.name, enemy.name)
				if chance.attempt(50):
					print "%s, momentarily distracted by shiny gold coins, loses track of %s and wanders off." % (enemy.name, player.name)
					player.setState(Player.STATE_EXPLORING)
					enemy = None
				else:
					print "The gold coins bounce off %s's body and clink to the ground. %s seems unimpressed." % (enemy.name, enemy.name)
			else:
				print "Sadly, %s has no gold to negotiate with..." % (player.name)
		else:
			print "What are you trying to negotiate with?"
		# skipInput = False

	elif command == "exit" or command == "x":
		break

	elif command == "?":
		printCommands()
		# skipInput = False

	else:
		print "I don't understand you."
		# skipInput = False

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
