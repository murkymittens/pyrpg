from room import Room
from util import happens
from random import randint

class RandomEventRoom(Room):
	def __init__(self):
		super(RandomEventRoom, self).__init__(Room.TYPE_RANDOM_EVENT)

	def interact(self, player, command):
		if happens(20):
			player.setHealthPotions(player.getHealthPotions() + 1)
			print "{player} found a health potions. You now have {pots} health potions.".format(player=player.name, pots=player.getHealthPotions())

		elif happens(10):
			reward = randint(5, 50)
			if happens(50):
				print "{player} found {gold} gold.".format(player=player.name, gold=reward)
				player.setGold(player.getGold() + reward)
			else:
				print "{player} found an ancient artifact and gained {exp} EXP.".format(player=player.name, exp=reward)
				player.setExperience(player.getExperience() + reward)
		
		elif happens(5):
			player.setHealth(player.getHealth() * 0.25)
			if player.getHealth() < 1:
				player.setHealth(1)
			print "You were careless and fell into a hole."
			player.announceHealth()
		
		elif happens(5):
			if happens(50) and player.getGold() > 0:
				player.setGold(player.getGold() * 0.5)
				print "Your pockets feel lighter. You feel around your gold purse and notice you have {gold} gold.".format(gold=player.getGold())
			elif player.getHealthPotions() > 0:
				player.setHealthPotions(player.getHealthPotions() * 0.75)
				print "Your pockets feel lighter. You feel around your potions bag and notice you have {pots} potions.".format(pots=player.getHealthPotions())
		else:
			if player.getHealth() < player.getMaximumHealth():
				player.setHealth(player.getHealth() + 1)
				print "{playerName} has recovered 1 HP.".format(playerName=player.name)
			player.setExperience(player.getExperience() + 1)
			print "{playerName} got 1 EXP.".format(playerName=player.name)
		
		self.passable = True
		return True
