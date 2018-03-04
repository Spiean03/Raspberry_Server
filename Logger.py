import Adafruit_DHT
import datetime
import time

SENSOR = Adafruit_DHT.DHT11
PIN = 4

class update():
  def temperature(self):
    humidity, temperature = Adafruit_DHT.read_retry(SENSOR,PIN)
    if humidity is not None and temperature is not None:
      self.humid = humidity
      self.temperature = temperature
    else:
      self.humid = None
      self.temp = None

u = update()
next_check = time.time()
s = 0
while True:
  if time.time() > next_check:
    try:
      u.temperature()
      t = datetime.datetime.now()
      t = datetime.datetime.strftime(t, '%Y-%m-%d %H:%M:%S')
      file = open('data.txt', 'a')
      file.write(str(t)+'\t'+str(u.temp)+'\t'+str(u.humid)+'\n')
      file.close()
      file2 = open('../../var/www/html/data.txt','a')
      file2.write(str(t)+'\t'+str(u.temp)+'\t'+str(u.humid)+'\n')
      file2.close()
      print 'data updated'
      s = 0
      next_check = time.time()+360
    except (RuntimeError,TypeError,NameError):
      s += 1
      print 'try again... %s' %s
      time.sleep(5)
