# -*- coding:utf-8 -*-
from flask import Flask, request
from time import sleep
import os, sys
reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__, static_folder='public', static_url_path='/public')
app.debug = True

SCHEDULE_FILE = '%s/schedule.txt' % os.path.dirname(os.path.abspath(__file__))

DURATION = 1
MODE = 'off'

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
    MODE = onoff
    sleep(DURATION)
    return MODE

def result(str, callback):
    result = '{"result": "%s"}' % str
    if callback is not '':
        result = '%s(%s);' % (callback, result)
    return result, 200, {'Content-Type': 'application/javascript; charset=utf-8'}

if __name__ == '__main__':
    app.run(host='0.0.0.0')
