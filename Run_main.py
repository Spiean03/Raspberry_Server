# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 16:10:01 2017
@author:    Andreas Spielhofer
            Ph.D. Candidate
            Physics Departement
            McGill University
            Montreal, Canada
@contact:   andreas.spielhofer@mail.mcgill.ca
"""

import os
import urllib2
import numpy as np
import datetime as dt
import time
import random


# Load MKS937B Controller
import MKS937B
mks = MKS937B.MKS()

#Load DHT11 Sensor
import DHT_logger
dht = DHT_logger.DHT_Sensor()


# Prepare the Max31855 GPIO pinouts:
import max31855 as max
cs_pins = [17, 18, 24, 25]
clock_pin = 23
data_pin = 22
units = "c"
thermocouples = []
for cs_pin in cs_pins:
    thermocouples.append(max.MAX31855(cs_pin, clock_pin, data_pin, units))
thermocouple_temperatures=[]



x_start = 0
x = []
y_main= []
y_prep= []

#x_start = dt.datetime.now()

#while True:
#
#
#    time.sleep(10)
#
#    x_now = dt.datetime.now()
#    if x_now >= x_start+dt.timedelta(minutes=1):
#        print "hello"
#        print x_now-x_start
#        x_start=dt.datetime.now()

next_check = time.time()
time.sleep(1)

running = True
while running == True:
      if time.time() > next_check:
                x_datetime = dt.datetime.now()
                x_datetime = dt.datetime.strftime(x_datetime,'%Y-%m-%d %H:%M:%S')
                #Get Data from DHT11 Sensor:
                try:
                        dht.temperature()

                except (RuntimeError, TypeError, NameError):
                        dht.temp = None
                        dht.humid = None
                        print "couldnt connect to DHT11"
                        
                #Get Data from MKS937B:              
                try:
                        mks.measure()
                except (RuntimeError, TypeError, NameError):
                        mks.main = None
                        mks.prep = None
                        print 'couldnt connect to MKS'
                
                #Get Data from Thermocouples:
                thermocouple_temperatures =''
                for thermocouple in thermocouples:
                        rj = thermocouple.get_rj()       
                        try:
                                    tc = thermocouple.get()
                                    thermocouple_temperatures += '\t'+str(tc)
                        except max.MAX31855Error as e:
                                    tc = None
                                    thermocouple_temperatures += '\t' +str(tc)  
                        print("tc: {} and rj: {}".format(tc, rj))

                #Save the data aquired from the sensors/controllers:
                f = open("/var/www/html/data.txt", 'a')
                f.write(str(x_datetime)+'\t'+str(mks.main)+'\t'+str(mks.prep)+'\t'+str(dht.temp)+'\t'+str(dht.humid)+thermocouple_temperatures+'\n')
                f.close()
next_check = time.time()+600 #wait another 600sec
