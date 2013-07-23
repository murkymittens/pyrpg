class Room(object):
	TYPE_GENERIC = 0
	TYPE_MONSTER = 1
	TYPE_SHOP = 2
	TYPE_RANDOM_EVENT = 3

	def __init__(self, type):
		self.type = type
		self.passable = False

	def interact(self, player, command):
		raise NotImplementedError

	def isPassable(self):
		return self.passable

class GenericRoom(Room):
	def __init__(self):
		super(GenericRoom, self).__init__(Room.TYPE_GENERIC)

	def interact(self, player, command):
		if player.getHealth() < player.getMaximumHealth():
			player.setHealth(player.getHealth() + 1)
			print "{playerName} has recovered 1 HP.".format(playerName=player.name)
		player.setExperience(player.getExperience() + 1)
		print "{playerName} got 1 EXP.".format(playerName=player.name)
		self.passable = True
		return True