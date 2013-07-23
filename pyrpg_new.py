from player import Player
from util import happens
from monsterroom import MonsterRoom
from randomeventroom import RandomEventRoom
from room import GenericRoom
from shoproom import ShopRoom
from time import sleep

def printCommands():
	print "Please use 'e' to explore, 'a' to attack, 'b' to buy potions, 'sb' to activate your shield bubble, 'h' to heal, 'n' to negotiate, or 'x' to commit suicide."

name = raw_input("What is your name, brave adventurer? ")
player = Player(name)
lastCommand = None
skipInput = False
room = None
stepsTaken = 0
monstersEncountered = 0
command = "e"

print ''
print "Welcome to the most evil dungeon you will ever face {player}!".format(player=player.name)
printCommands()
print "Should you find this dungeon too...hard, feel free to commit suicide and end your eternal damnation on earth \
and begin your eternal damnation in hell. *cackle*"
print ''

while player.isAlive():
	if room == None or room.isPassable():
		if happens(10):
			room = MonsterRoom(stepsTaken, monstersEncountered)
			monstersEncountered = monstersEncountered + 1
		elif happens(10):
			room = ShopRoom()
		else:
			room = RandomEventRoom()
			room.interact(player, None)
			skipInput = True

	if not skipInput:
		print ''
		command = raw_input("What do you want to do? ")
	else:
		skipInput = False
	
	if len(command) == 0 and lastCommand != None:
		command = lastCommand

	if not room.interact(player, command):
		print "You can't do that right now."

	if command == "exit" or command == "x":
		break
	elif command == "?":
		printCommands()
	lastCommand = command
	sleep(0.5)