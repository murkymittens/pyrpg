from room import Room

class ShopRoom(Room):
	def __init__(self):
		super(ShopRoom, self).__init__(Room.TYPE_SHOP)
		print "You've stumbled across a rickety shack. There appear to be items for sale..."

	def interact(self, player, command):
		if command == "buy" or command == "b":
			splitCommand = command.split(' ', 1)
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
			return True
		elif command == "explore" or command == "e":
			self.passable = True
			return True
		else:
			return False