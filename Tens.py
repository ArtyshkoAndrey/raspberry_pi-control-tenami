import time
import RPi.GPIO as GPIO

class Tens():
	def __init__(self):
		self.tena1 = False
		self.tena2 = False
		self.tena3 = False
		self.TimeSleep = 2
		self.crTena = 0
		self.CountTena = 0
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(19,GPIO.OUT) # Тена 3
		GPIO.setup(20,GPIO.OUT) # Тена 2
		GPIO.setup(21,GPIO.OUT) # Тена 1
		GPIO.output(20,GPIO.LOW)
		GPIO.output(19,GPIO.LOW)
		GPIO.output(21,GPIO.LOW)

	# Потоковый метод для двух тэн
	def TwoHeaters(self):
		# Алгоритм переключения тэн
		self.TwoHeatersBlink(self.crTena, self.CountTena)

		self.crTena += 1
		self.CountTena += 1
		# Зброс счётчика
		if self.crTena == 3:
			self.crTena = 0
		if self.CountTena == 3:
			self.CountTena = 0

		print(self.tena1)
		print(self.tena2)
		print(self.tena3)
		print(self.TimeSleep)
		print("--------")
		time.sleep(self.TimeSleep)
	
	# Алгоритм переключения тен
	def TwoHeatersBlink(self, currentTena, counterTenaPin):
		# Отключаем не нужную тэну
		if currentTena == 0:
			self.tena2 = False
			GPIO.output(20,GPIO.LOW)
		elif currentTena == 1:
			self.tena3 = False
			GPIO.output(19,GPIO.LOW)
		else:
			self.tena1 = False
			GPIO.output(21,GPIO.LOW)
		# Включем нужную тэну
		if counterTenaPin == 0:
			self.tena1 = True
			GPIO.output(21,GPIO.HIGH)
		elif counterTenaPin == 1:
			self.tena2 = True
			GPIO.output(20,GPIO.HIGH)
		else:
			self.tena3 = True
			GPIO.output(19,GPIO.HIGH)
