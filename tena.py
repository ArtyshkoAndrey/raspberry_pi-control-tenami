import time

class Tens():
	def __init__(self):
		self.tena1 = False
		self.tena2 = False
		self.tena3 = False

		self.crTena = 0
		self.CountTena = 0

	def blink(self):

		self.toggleTenaBlink(self.crTena, self.CountTena)

		self.crTena += 1
		self.CountTena += 1

		if self.crTena == 3:
			self.crTena = 0

		if self.CountTena == 3:
			self.CountTena = 0

		print(self.tena1)
		print(self.tena2)
		print(self.tena3)
		time.sleep(5)
	

	def toggleTenaBlink(self, currentTena, counterTenaPin):
		if currentTena == 0:
			self.tena2 = False
		elif currentTena == 1:
			self.tena3 = False
		else:
			self.tena1 = False

		if counterTenaPin == 0:
			self.tena1 = True
		elif counterTenaPin == 1:
			self.tena2 = True
		else:
			self.tena3 = True