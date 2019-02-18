from Tens import Tens
from time import sleep
from raspberry import RaspberryThread
from array import array
from datetime import datetime, time
from Temperature import read_temp

class SmartSystem():
	def __init__(self):
		self.Tens = Tens()
		self.TwoHeaters = None
		# collect threads
		self.threads = [
			self.TwoHeaters
		]
		self.cheked = False
		# Третий элемент то checkbox если отключили что бы тэны включались в данное время
		self.times = [[2, 11, True], [14, 20, True], [21, 1, True]]
		self.temp = [28, 30]
		self.tempnow = None

	def loop(self):
		self.tempnow = read_temp("28-000006dde2ec")
		print("Массив температуры", self.temp)
		print("Температура отопления", self.tempnow)
		# Время в данный момент
		now = datetime.now().time()
		counter = 0

		for timer in self.times:
			if timer[0] < timer[1]:
				if (now >= time(timer[0], 00) and now <= time(timer[1], 00)) and timer[2] == True:
					counter += 1
			else:
				if (now >= time(timer[0], 00) or now <= time(timer[1], 00)) and timer[2] == True:
					counter += 1

		if counter != 0:
			# Запуск тэн если прошло время
			if self.cheked == False:
				# Запуск если первый раз запустили системы
				if not self.TwoHeaters.isAlive():
					# Запуск потока если не запускался ни разу
					self.TwoHeaters.start()
				# Возобновляем потомк так как по умолчию он остановлен
				self.TwoHeaters.resume()
				# Меняем на True так как поток уже запущен
				self.cheked = True
			if self.tempnow > self.temp[1]:
				print("Не прошло по температуре")
				if self.cheked != False:
					self.cheked = False
					self.TwoHeaters.pause()
					self.Tens.OffHeaters()
			elif self.tempnow < self.temp[0]:
				print("Прошло по температуре")
				# Запуск тэн если прошло время
				if self.cheked == False:
					# Запуск если первый раз запустили системы
					if not self.TwoHeaters.isAlive():
						# Запуск потока если не запускался ни разу
						self.TwoHeaters.start()
					# Возобновляем потомк так как по умолчию он остановлен
					self.TwoHeaters.resume()
					# Меняем на True так как поток уже запущен
					self.cheked = True
		else:
			print("Не прошло по времени")
			if self.cheked != False:
				self.cheked = False
				self.TwoHeaters.pause()
				self.Tens.OffHeaters()

		# Остановка по времени
		print("Остановка --------------- ")
		sleep(5)

	def setTens(self):
		self.TwoHeaters = RaspberryThread(function=self.Tens.TwoHeaters)
		self.TwoHeaters.setDaemon(True)
		print(self.TwoHeaters.isDaemon())