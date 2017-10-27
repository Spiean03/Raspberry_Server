# -*- coding: utf-8 -*-
"""
Created on Fri Oct 20 16:10:01 2017

@author:    Andreas Spielhofer
            Ph.D. Candidate
            Physics Departement
            McGill University
            Montreal, Canada
@contact:   andreas.spielhofer@mail.mcgill.ca


Directions:
            
"""

import os
import urllib2
import numpy as np
import datetime as dt
import time
import random
import MKS937B
import matplotlib.dates as mdates
import pandas as pd
#myFmt = mdates.DateFormatter('%d')

from bokeh.models import DatetimeTickFormatter
from bokeh.plotting import figure, show, output_file, save
from bokeh.palettes import Spectral11
mks = MKS937B.MKS()
dht = DHT_Sensor()

x_start = 0
x = []
y_main= []
y_prep= []

#x_start = datetime.datetime.now()

#while True:
#
#
#    time.sleep(10)
#
#    x_now = datetime.datetime.now()
#    if x_now >= x_start+datetime.timedelta(minutes=1):
#        print "hello"
#        print x_now-x_start
#        x_start=datetime.datetime.now()

while True:  
    
    x_datetime=dt.datetime.now()
    print x_datetime
    x_datetime = dt.datetime.strftime(x_datetime,'%Y-%m-%d %H:%M:%S')
    m.measure()
    
    x.append(x_datetime)
    #print x
    
    y_random = random.randint(1,10000)
    
    #y_main.append(m.main)
    #y_prep.append(m.prep)
    
    f = open("data_pressure.txt", 'a')
    f.write(str(x_datetime)+'\t'+str(m.main)+'\t'+str(m.prep)+'\n')
    f.close()
    data = pd.read_csv("data_pressure.txt",sep='\t', header = None)
    data.columns =["time","main","prep"]
    try:
        data2 = pd.read_csv("http://132.206.186.19/data.txt",sep='\t', header = None)
        data2.columns =["time2","temp", "humid"]
    except urllib2.URLError:
        print "Couldn't connect to Raspberry Pi"        
    x1 = []
    x2 = []
    y_main= []
    y_prep= []
    y_temp = []
    y_humid = []
    for element in data["time"]:
        new = dt.datetime.strptime(element,'%Y-%m-%d %H:%M:%S')
        x1.append(new)
    for element in data["main"]:
        y_main.append(element)
    for element in data["prep"]:
        y_prep.append(element)
        
     #for the temperature:
    try:
        for element in data2["time2"]:
        
            new2 = dt.datetime.strptime(element,'%Y-%m-%d %H:%M:%S')
            x2.append(new2)
        for element in data2["temp"]:
            y_temp.append(element)
        for element in data2["humid"]:
            y_humid.append(element)
    except NameError:
        print "Couldn't connect to Raspberry Pi"
#    print x_day
#    x_month=datetime.datetime.now().strftime('%m')
#    print x_month
#    x = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
#    print x
    
    
    #x = np.linspace(0.1, 5, 100)
    p = figure(title="UHV System - Pressure", x_axis_type = "datetime", y_axis_type="log",
               y_range=(1E-11, 1000), plot_width = 800, plot_height = 600)
#    p.xaxis.formatter = DatetimeTickFormatter(
#        hours=["%d %B %Y"],
#        days=["%d %B %Y"],
#        months=["%d %B %Y"],
#        years=["%d %B %Y"],
#    )
    p.line(x1, y_main, legend="Pressure Main",
           line_color=Spectral11[1], line_dash="dashed", line_width = 3)
    p.line(x1, y_prep, legend="Pressure Prep",
           line_color=Spectral11[2], line_dash="dashed", line_width=3) 

    p.line(x2, y_temp, legend="Temperature",
           line_color=Spectral11[3], line_dash="dashed", line_width=3)
    p.line(x2, y_humid, legend="Humidity",
           line_color=Spectral11[4], line_dash="dashed", line_width=3)   

       
#    p.text_font="calibri" 
#    p.text_font_size="13" 
#    p.text_font_style="normal"
           
#    p.circle(x, x, legend="y=x")
#    
#    p.line(x, x**2, legend="y=x**2")
#    p.circle(x, x**2, legend="y=x**2",
#             fill_color=None, line_color="olivedrab")
#    
#    p.line(x, 10**x, legend="y=10^x",
#           line_color="gold", line_width=2)
#    
#    p.line(x, x**x, legend="y=x^x",
#           line_dash="dotted", line_color="indigo", line_width=2)
#    
#    p.line(x, 10**(x**2), legend="y=10^(x^2)",
#           line_color="coral", line_dash="dashed", line_width=2)
#    
    p.legend.location = "top_left"
    
    p.xaxis.axis_label = 'Time'
    p.yaxis.axis_label = 'Pressure (mbar)'
    
    output_file("logplot2.html", title="Pressure over Time")
    print "done"
    save(p)
    time.sleep(900)
    #x_start += 900
    #show(p)  # open a browser
