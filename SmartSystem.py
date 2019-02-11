from time import sleep
from Tens import Tens
from raspberry import RaspberryThread
from array import array
from datetime import datetime

class SmartSystem():
	def __init__(self, TimeSleep = 1):
		self.TimeSleep = TimeSleep
		self.Tens = Tens()
		self.TwoHeaters = RaspberryThread(function=self.Tens.TwoHeaters)
		# collect threads
		self.threads = [
			self.TwoHeaters
		]
		self.cheked = False
		# Третий элемент то checkbox если отключили что бы тэны включались в данное время
		self.times = [[11, 2, 1], [3, 5, 0], [6, 9, 1]]

	def loop(self):
		# Время в данный момент, час
		now = int(datetime.now().strftime('%H'))

		for time in self.times:
			if (now >= time[0] or now <= time[1]) and time[2] == 1:
				# Запуск тэн если прошло время
				if self.cheked == False:
					# Запуск если первый раз запустили системы
					if not self.TwoHeaters.isAlive() or self.TwoHeaters.paused == True:
						# Запуск потока если не запускался ни разу
						self.TwoHeaters.start()
					# Возобновляем потомк так как по умолчию он остановлен
					self.TwoHeaters.resume()
					# Меняем на True так как поток уже запущен
					self.cheked = True

		# Остановка по времени
		sleep(self.TimeSleep)