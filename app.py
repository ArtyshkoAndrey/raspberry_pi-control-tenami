from flask import Flask, render_template, request, jsonify
from raspberry import RaspberryThread
from time import sleep
from SmartSystem import SmartSystem
import datetime

app = Flask(__name__)

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
        dictToReturn = {'system': 'on'}
        return jsonify(dictToReturn)

# Маршрут отключение системы и всех потоков
@app.route("/stop", methods=['POST'])
def stop():
    if request.method == 'POST':
        # Дописать метод и вызов его, отключение потоков в system
        Smart.pause()
        System.TwoHeaters.pause()
        System.cheked = False
        dictToReturn = {'system': 'off'}
        return jsonify(dictToReturn)

# Получение всех данных для spa
@app.route("/status", methods=['POST'])
def status():
    if request.method == 'POST':
        now = datetime.datetime.now()
        dateNow = now.strftime("%Y-%m-%d")
        timeNow = now.strftime("%H:%M")
        if not Smart.paused:
            dictToReturn = "on"
        else:
            dictToReturn = "off"
        response = {
            'system': dictToReturn,
            'date': dateNow,
            'time': timeNow
        }
        return jsonify(response)

if __name__ == '__main__':
    # Создание обьекта и потока
    System = SmartSystem()
    Smart = RaspberryThread(function=System.loop)

    # Коллекция потоков
    threads = [
        Smart,
    ]

    # Запуск сервера
    app.run( debug=True, host="0.0.0.0", port="80", threaded=True)