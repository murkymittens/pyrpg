class Skill:
	def __init__(self, name = "Generic Skill", cooldownPeriod = 0):
		self.name = name
		self.active = False
		self.cooldownPeriod = cooldownPeriod
		self.cooldown = 0

	def update(self):
		if self.active:
			if self.cooldownPeriod > 0:
				self.cooldown = self.cooldown - 1
				if self.cooldown == 0:
					self.active = False

	def activate(self):
		if not self.active:
			self.active = True
			self.cooldown = self.cooldownPeriod

	def deactivate(self):
		self.active = False

	def getCooldown(self):
		return self.cooldown

class SimpleBuff:
	def __init__(self, name, duration, cooldown):
		self.name = name
		self._duration = duration
		self._cooldown = cooldown
		self.active = False
		self.duration = 0
		self.cooldown = 0

	def activate(self):
		self.active = True
		self.cooldown = self._cooldown
		self.duration = self._duration

	def update(self):
		self.cooldown = self.cooldown - 1
		if self.cooldown < 0:
			self.cooldown = 0

		if self.active:
			self.duration = self.duration - 1
			if self.duration == 0:
				self.active = False

	def reset(self):
		self.active = False
		self.cooldown = 0
		self.duration = 0
