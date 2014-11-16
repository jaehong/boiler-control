from flask import Flask, redirect, request, current_app
import json
from functools import wraps
from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

PIN_PWM = 18
PIN_SIG = 23
DURATION = 1
SPEED = 100
MODE = 'off'

GPIO.setup(PIN_SIG, GPIO.OUT)
GPIO.setup(PIN_PWM, GPIO.OUT)

p = GPIO.PWM(PIN_PWM, SPEED)

app = Flask(__name__)

@support_jsonp
@app.route('/')
def hello():
    return jsonify({"status": MODE})

@support_jsonp
@app.route('/on')
def turn_on():
    return jsonify({"status": MODE})

@support_jsonp
@app.route('/off')
def turn_off():
    return jsonify({"status": MODE})

def turn(onoff):
    global MODE
    if onoff is 'off':
        GPIO.output(PIN_SIG, GPIO.LOW)
    else:
        GPIO.output(PIN_SIG, GPIO.HIGH)
    MODE = onoff
    p.start(SPEED)
    sleep(DURATION)
    p.stop()
    return MODE

def support_jsonp(f):
    """Wraps JSONified output for JSONP"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        callback = request.args.get('callback', False)
        if callback:
            content = str(callback) + '(' + str(f(*args,**kwargs).data) + ')'
            return current_app.response_class(content, mimetype='application/javascript')
        else:
            return f(*args, **kwargs)
    return decorated_function

if __name__ == '__main__':
    app.run(host='0.0.0.0')
