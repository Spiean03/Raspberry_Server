import time
import Adafruit_DHT
import datetime
import RPi.GPIO as GPIO

#SENSOR = Adafruit_DHT.DHT11 #define what sensor being used
#PIN = 4 #define pin from Raspberry

class DHT_Sensor():
  def __init__(self):
	self.SENSOR = Adafruit_DHT.DHT11 #define what sensor being used
	self.PINA = 4 #define pin from Raspberry
  def temperature(self):
    humidity, temperature = Adafruit_DHT.read_retry(self.SENSOR,self.PINA)

    if humidity is not None:
      self.humid = humidity
    else:
      self.humid = None
      
    if temperature is not None:
      self.temp = temperature 
    else:
      self.temp = None

      
