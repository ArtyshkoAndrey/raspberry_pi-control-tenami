from time import sleep
from tena import Tens
from raspberry import RaspberryThread

class SmartSystem():
	def __init__(self, TimeSleep = 1):
		self.TimeSleep = TimeSleep
		self.tens = Tens()
		self.blink = RaspberryThread(function=self.tens.blink)
		# collect threads
		self.threads = [
			self.blink
		]
		self.cheked = False

	def loop(self):
		if self.cheked == False:
			if not self.blink.isAlive():
				self.blink.start()
			self.blink.resume()
			self.cheked = True
		sleep(self.TimeSleep)