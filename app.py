from flask import Flask, render_template, request, jsonify
from raspberry import RaspberryThread
import os
from time import sleep
from tena import test
import datetime

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/blink", methods=['POST'])
def blink_view():
    if request.method == 'POST':
        # Pause any running threads
        any(thread.pause() for thread in threads)
        # Start the target thread if it is not running
        if not testecho.isAlive():
            testecho.start()
        # Unpause the thread and thus execute its function
        testecho.resume()
        dictToReturn = {'system': 'on'}
        return jsonify(dictToReturn)

@app.route("/stop", methods=['POST'])
def stop():
    if request.method == 'POST':
        testecho.pause()
        dictToReturn = {'system': 'off'}
        return jsonify(dictToReturn)

@app.route("/status", methods=['POST'])
def status():
    if request.method == 'POST':
        now = datetime.datetime.now()
        dateNow = now.strftime("%Y-%m-%d")
        timeNow = now.strftime("%H:%M")
        print(not testecho.paused)
        if not testecho.paused:
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
    # Create threads
    testecho = RaspberryThread(function=test)

    # collect threads
    threads = [
        testecho,
    ]

    # Run server
    app.run( debug=True, host="0.0.0.0", port="80", threaded=True)