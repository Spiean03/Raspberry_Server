import time
import Adafruit_DHT
import datetime

SENSOR = Adafruit_DHT.DHT11 #define what sensor being used
PIN = 4 #define pin from Raspberry

def temperature():
  global temperature
  global humidity
  humidity, temperature = Adafruit_DHT.read_retry(SENSOR,PIN)
  
  if humidity is not None and temperature is not None:
    return temperature, humidity
  else:
    humidity = None
    temperature = None
    return temperature, humidity
 
next_check = time.time()
time.sleep(1)

while True:
  if time.time() > next_check:
    temperature()
    t = datetime.datetime.now()
    file = open("data.txt",a)
    file.write(str(t)+'\t'+str(temperature)='\t'+str(humidity)+'\n')
    file.close()
    print "data updated"
    next_check = time.time()+600 #wait another 600sec
