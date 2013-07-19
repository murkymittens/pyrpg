from skill import Skill

class Buff(Skill):
	def __init__(self, name, duration = 0, cooldownPeriod = 0):
		Skill.__init__(self, name, cooldownPeriod)
		self.duration = duration

	def update(self):
		Skill.update(self)
		if self.active:
			self.duration = self.duration - 1
			if self.duration == 0:
				self.deactivate()

class ShieldBubble(Buff):
	def __init__(self):
		Buff.__init__("Shield Bubble", 5, 8)

	def act(self, damage):
		return 0