# -*- coding:utf-8 -*-
# DHT11 로 온도를 기록한다.
# schedule.txt를 읽어 실행해야 할때 실행 한다.
import os, sys, time, subprocess
reload(sys)
sys.setdefaultencoding("utf-8")
SCHEDULE_FILE = '%s/schedule.txt' % os.path.dirname(os.path.abspath(__file__))

def main():
  f = open(SCHEDULE_FILE, 'r')
  now = time.strftime('%H:%M')

  lines = f.readlines()
  f.close()
  for line in lines:
    stime, how = line.replace("\n",'').replace('켬','on').replace('끔','off').split(' ')
    if(stime == now):
      print subprocess.check_output('/usr/bin/curl -s http://localhost:5000/%s?via_cron' % how, shell=True)

if __name__ == '__main__':
  main()