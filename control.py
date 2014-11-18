# -*- coding:utf-8 -*-
from flask import Flask, request
import RPi.GPIO as GPIO
from time import sleep
import os, sys

reload(sys)
sys.setdefaultencoding("utf-8")

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

PIN_PWM = 18
PIN_SIG = 23
DURATION = 1
SPEED = 100
MODE = 'off'
SCHEDULE_FILE = '%s/schedule.txt' % os.path.dirname(os.path.abspath(__file__))

GPIO.setup(PIN_SIG, GPIO.OUT)
GPIO.setup(PIN_PWM, GPIO.OUT)

p = GPIO.PWM(PIN_PWM, SPEED)

app = Flask(__name__, static_folder='public', static_url_path='/public')

@app.route('/')
def hello():
    callback = request.args.get('callback', '')
    return result(MODE, callback)

@app.route('/on')
def turn_on():
    callback = request.args.get('callback', '')
    return result(turn('on'), callback)

@app.route('/off')
def turn_off():
    callback = request.args.get('callback', '')
    return result(turn('off'), callback)

@app.route('/get_schedule')
def get_schedule():
    callback = request.args.get('callback', '')
    if not os.path.exists(SCHEDULE_FILE):
        open(SCHEDULE_FILE, 'w').close()
    f = open(SCHEDULE_FILE, 'r')
    data = f.read()
    f.close()
    return result(data.replace("\n",'\\n'), callback)

@app.route('/set_schedule', methods=['post'])
def set_schedule():
    data = request.form['data']
    f = open(SCHEDULE_FILE, 'w')
    f.write(data.replace("\\n","\n"))
    f.close()
    return '분부대로 하겠나이다.'

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

def result(str, callback):
    result = '{"result": "%s"}' % str
    if callback is not '':
        result = '%s(%s);' % (callback, result)
    return result, 200, {'Content-Type': 'application/javascript; charset=utf-8'}

if __name__ == '__main__':
    app.run(host='0.0.0.0')
