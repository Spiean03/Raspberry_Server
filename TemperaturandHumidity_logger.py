import time
import Adafruit_DHT
import datetime

SENSOR = Adafruit_DHT.DHT11 #define what sensor being used
PIN = 4 #define pin from Raspberry

class update():
  def __init__(self):
		  self.SENSOR = Adafruit_DHT.DHT11 #define what sensor being used
      self.PIN = 4 #define pin from Raspberry
  def temperature(self):
    humidity, temperature = Adafruit_DHT.read_retry(self.SENSOR,self.PIN)

    if humidity is not None:
      self.humid = humidity
    else:
      self.humid = None
      
    if temperature is not None:
      self.temp = temperature 
    else:
      self.temp = None

next_check = time.time()
time.sleep(1)
s=0
u = update()
while True:
  if time.time() > next_check:
    try:
      u.temperature()
      t = datetime.datetime.now()
      file = open("data.txt",a)
      file.write(str(t)+'\t'+str(u.temp)='\t'+str(u.humid)+'\n')
      file.close()
      print "data updated"
      next_check = time.time()+600 #wait another 600sec
      s = 0
    except (RuntimeError, TypeError, NameError):
      s+=1
      print "try again... %s" %s
      time.sleep(5)
      
