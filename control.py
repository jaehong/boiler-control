from flask import Flask, request
import RPi.GPIO as GPIO
from time import sleep

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


@app.route('/')
def hello():
    callback = request.args.get('callback', '')
    return return_result(MODE, callback)

@app.route('/on')
def turn_on():
    callback = request.args.get('callback', '')
    return return_result(turn('on'), callback)

@app.route('/off')
def turn_off():
    callback = request.args.get('callback', '')
    return return_result(turn('off'), callback)

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

def return_result(str, callback):
    result = '{"status": "%s"}' % str
    if callback is '':
        return result
    else:
        return '%s(%s);' % (callback, result)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
