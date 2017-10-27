"""
Created on Tue May 19 14:29:57 2015

@author:    Andreas Spielhofer
            Ph.D. Candidate
            Physics Departement
            McGill University
            Montreal, Canada
@contact:   andreas.spielhofer@mail.mcgill.ca


Directions: Call MKS() class to initialize it:
            m = MKS()

            when you call m.measure(), it will print the pressure in main and prep. The two values can then be used by printing 
            print m.main 
            print m.pressure
"""

import serial as _s
import time
import sys

#param={'P1':'mbar','P3':'mbar','P5':'mbar','P6':'mbar'}

class MKS():  
    
    def __init__(self, port=None):
        print "Now initializing"
        try:
            print "Trying hard"
            if port is None:
                print 'here1'
                self._serial = _s.Serial(port = 'COM8', baudrate = 9600,bytesize=_s.EIGHTBITS, parity = _s.PARITY_NONE, xonxoff = False, stopbits = _s.STOPBITS_ONE, timeout = 2)
                print 'here2'                
                print self._serial.name
            else:
                print "tried, could not connect"
        except:
            self._serial.close()
            raise RuntimeError('Could not open serial connection')

        if self._serial is None:
            raise RuntimeError('Could not open serial connection')
            print "did not work"
        print("initialized")
#        print('NexTorr Controller initialized on port %s' %self._serial.name)
#        self._serial.write('V\r')
#        print('Firmware Version: ' + self._serial.readline())
#        self._serial.write('TS\r')
#        print('Status: ' + self._serial.readline())    


    def measure(self):
        stri="@253"+"PRZ?"+";FF\r\n"
        print stri
        self.pressure = self._serial.write(stri)
        pressure = self._serial.readline()
        print pressure # This normally gives a return in the form of @253ACK2.10E-09 NOGAUGE 4.50E-07 NOGAUGE LO<E-03 LO<E-03;FF
        pressure = pressure.replace("@253ACK","") # remove it from the string
        pressure = pressure.replace(";FF","") # remove it from the string
        self.pressure = pressure.split(" ")
        print self.pressure #where self.pressure[0], [2] are the pressures of the ion gauges and self.pressure[4] and [5] are the ones from the Pirani
        if self.pressure[0] == "OFF" or self.pressure[0] == "NOGAUGE":
            if self.pressure[4] == "LO<E-03" or self.pressure[4] == "OFF" or self.pressure[4] == "NOGAUGE":
                print "Main = 1000"
                self.main = float(1000)
            else:
                print "Main = %s" %  self.pressure[4]
                self.main = float(self.pressure[4])
            
        else:
            print "Main = %s" % self.pressure[0]
            self.main = float(self.pressure[0])
        
        if self.pressure[2] == "OFF" or self.pressure[2] == "NOGAUGE":
            if self.pressure[5] == "OFF" or self.pressure[5] == "NOGAUGE":
                print "Prep = 1000"
                self.prep = float(1000)
            else:
                print "Prep = %s" % float(self.pressure[5])
                self.prep = float(self.pressure[5])
        else:
            print "Prep = %s" %  self.pressure[2]
            self.prep = float(self.pressure[2])
