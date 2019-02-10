from flask import Flask, render_template
from raspberry import RaspberryThread
import os
from time import sleep

def test():
	print('Test theard')
	sleep(2)


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/blink", methods=['GET'])
def blink_view():
    # Pause any running threads
    any(thread.pause() for thread in threads)
    # Start the target thread if it is not running
    if not testecho.isAlive():
        testecho.start()
    # Unpause the thread and thus execute its function
    testecho.resume()
    return "testecho started"

@app.route("/stop", methods=['GET'])
def stop():
    any(thread.pause() for thread in threads)
    return "all threads paused"

if __name__ == '__main__':
    # Create threads
    testecho = RaspberryThread(function=test)

    # collect threads
    threads = [
        testecho,
    ]

    # Run server
    app.run( debug=True, host="0.0.0.0", port="80", threaded=True)