from flask import Flask, render_template, request, jsonify
from raspberry import RaspberryThread
from time import sleep
from SmartSystem import SmartSystem
import datetime
import os
from jsondb.db import Database
from DatabaseFunctions import save
from Temperature import read_temp
import RPi.GPIO as GPIO
import sys
import signal


db = Database("data.db")

app = Flask(__name__)


# Создание обьекта и потока
System = SmartSystem()
Smart = RaspberryThread(function=System.loop)

# Коллекция потоков
threads = [
    Smart,
]

System.times = db['system']['times']
System.Tens.TimeSleep = db['system']['timer']

System.setTens()
    
Smart.setDaemon(True)

if db['system']['system'] == 'on':
    if not Smart.isAlive():
        Smart.start()
    Smart.resume()
else:
    Smart.pause()
    
print("test")

# Если открыли главную то вывод spa
@app.route("/")
def index():
    return render_template("index.html")

# Включение потока главной системы
@app.route("/start", methods=['POST'])
def start():
    # Проверка на пост запрос
    if request.method == 'POST':
        # На паузу все потоки которые есть в массиве в данном файле
        any(thread.pause() for thread in threads)

        # Запуск потомка если не запускался
        if not Smart.isAlive():
            Smart.start()
        # Снятие потока с паузы
        Smart.resume()
        db['system']['system'] = 'on'
        dictToReturn = {'system': 'on'}
        save(db, Smart, System)
        return jsonify(dictToReturn)

# Маршрут отключение системы и всех потоков
@app.route("/stop", methods=['POST'])
def stop():
    if request.method == 'POST':
        # Дописать метод и вызов его, отключение потоков в system
        any(thread.pause() for thread in threads)
        System.TwoHeaters.pause()
        System.cheked = False
        System.Tens.OffHeaters()
        dictToReturn = {'system': 'off'}
        save(db, Smart, System)
        return jsonify(dictToReturn)

# Получение всех данных для spa
@app.route("/status", methods=['POST'])
def status():
    if request.method == 'POST':
        now = datetime.datetime.now()
        dateNow = now.strftime("%Y-%m-%d")
        timeNow = now.strftime("%H:%M")

        times = System.times

        if not Smart.paused:
            dictToReturn = "on"
        else:
            dictToReturn = "off"
        response = {
            'system': dictToReturn,
            'date': dateNow,
            'time': timeNow,
            'times': times,
            'timer': System.Tens.TimeSleep,
            'temp1': read_temp(),
            'temp2': read_temp(),
        }
        return jsonify(response)

@app.route("/tenatimes/<int:time1>/<int:time2>/<string:cheked>/<int:mode>", methods=['POST'])
def tenatimes(time1, time2, cheked, mode):
    if request.method == 'POST':
        System.times[mode][0] = int(time1)
        System.times[mode][1] = int(time2)
        if cheked == "true":
            System.times[mode][2] = True
        elif cheked == "false":
            System.times[mode][2] = False

        cmd = {
            'time1': System.times[mode][0],
            'time2': System.times[mode][1],
            'cheked': System.times[mode][2]
        }

        save(db, Smart, System)
        return jsonify(cmd)

@app.route("/timer/<int:minutes>", methods=['POST'])
def timer(minutes):
    # TODO что бы не приходилось дожидать конец прошлого таймера, 
    # необходимо удалять моток полностью и создавать заново с новым временем
    if request.method == 'POST':
        System.Tens.TimeSleep = minutes
        save(db, Smart, System)
        print(db['system']['timer'])

        cmd = {
            'timer': System.Tens.TimeSleep
        }

        return jsonify(cmd)

if __name__ == '__main__':
    # Запуск сервера
    app.run(host="0.0.0.0", port="80")
    def handler(signal, frame):
        print('CTRL-C pressed!')
        GPIO.cleanup()
        sys.exit(0)

    signal.signal(signal.SIGINT, handler)
    signal.pause()