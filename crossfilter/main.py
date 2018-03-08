import pandas as pd
import numpy as np
import datetime
from bokeh.layouts import row, widgetbox
from bokeh.models import Select
from bokeh.palettes import Spectral5,RdYlBu5,Plasma5, Colorblind5
from bokeh.plotting import curdoc, figure
from bokeh.sampledata.autompg import autompg_clean as df
#
#df = df.copy()
#data = pd.read_csv("Data_Pressure_Temp.csv", header = 1)
data = pd.read_csv("http://132.206.186.19/data.txt",delimiter='\t', header = 0)

data.columns =["time","main","LL","roomtemp","humidity",'t1','t2','t3','t4']
data["time"] = pd.to_datetime(data["time"])


SIZES = list(range(6, 22, 3))
COLORS = Spectral5

# data cleanup
#df.cyl = df.cyl.astype(str)
#df.yr = df.yr.astype(str)
#del df['name']
#
#columns = sorted(df.columns)
#discrete = [x for x in columns if df[x].dtype == object]
#continuous = [x for x in columns if x not in discrete]
#quantileable = [x for x in continuous if len(df[x].unique()) > 20]

columns2 = sorted(data.columns)
discrete2 = [x for x in columns2 if data[x].dtype == object]
continuous2 = [x for x in columns2 if x not in discrete2]
quantileable2 = [x for x in continuous2 if len(data[x].unique()) > 20]



def create_figure():
    #xs = data[x.value].values
    xs = data["time"].values

    if y.value =="Pressure Main and LoadLock":
        ys = data['main'].values
        yb = data['LL'].values
        yc = np.zeros(len(xs)) 
        yd = np.zeros(len(xs)) 
    elif y.value == "RoomTemp and Humidity":
        ys = data['roomtemp']
        yb = data['humidity']
        yc = np.zeros(len(xs)) 
        yd = np.zeros(len(xs)) 
    elif y.value == "Pressure Main":
        ys = data['main'].values
        yb = np.zeros(len(xs))
        yc = np.zeros(len(xs)) 
        yd = np.zeros(len(xs)) 
    elif y.value == "Pressure LoadLock":
        ys = data['LL'].values
        yb = np.zeros(len(xs))
        yc = np.zeros(len(xs)) 
        yd = np.zeros(len(xs))  
    elif y.value == 'Chamber Temperature':
        ys = data['t1']
        yb = data['t2']
        yc = data['t3']
        yd = data['t4']
    else:
        ys = data[y.value].values
        yb = np.zeros(len(xs))
        yc = np.zeros(len(xs)) 
        yd = np.zeros(len(xs)) 
    x_title = x.value.title()
    y_title = y.value.title()
    now = datetime.datetime.now()   
    if x.value == "Last 24hrs":
        val= 0
        index =0
        for element in data["time"]:
            a = now-element
            if datetime.timedelta(1.0125) >= a:
                val = index
                break
            index +=1
        xs = xs[val:]
        ys = ys[val:]
        yb = yb[val:]
        yc = yc[val:]
        yd = yd[val:]
    elif x.value == "Last 3 Days":
        val= 0
        index = 0
        for element in data["time"]:
            a = now-element
            if datetime.timedelta(3.0125) >= a:
                val = index
                break
            index +=1
        xs = xs[val:]
        ys = ys[val:]
        yb = yb[val:]
        yc = yc[val:]
        yd = yd[val:]
    elif x.value == "Last Week":
        val= 0
        index = 0
        for element in data["time"]:
            a = now-element
            if datetime.timedelta(7.0125) >= a:
                val = index
                break
            index +=1
        xs = xs[val:]
        ys = ys[val:]
        yb = yb[val:]
        yc = yc[val:]
        yd = yd[val:]
    elif x.value == "Last Month":
        val= 0
        index = 0
        for element in data["time"]:
            a = now-element
            if datetime.timedelta(31.0125) >= a:
                val = index
                break
            index +=1
        xs = xs[val:]
        ys = ys[val:]
        yb = yb[val:]
        yc = yc[val:]
        yd = yd[val:]        
    elif x.value == "Last 3 Months":
        val= 0
        index = 0
        for element in data["time"]:
            a = now-element
            if datetime.timedelta(93.0125) >= a:
                val = index
                break
            index +=1
        xs = xs[val:]
        ys = ys[val:]
        yb = yb[val:]
        yc = yc[val:]
        yd = yd[val:]
    else:
        xs = xs
        ys = ys
        yb = yb
        yc = yc
        yd = yd
    kw = dict()
    if x.value in discrete2:
        kw['x_range'] = sorted(set(xs))
    if y.value in discrete2:
        kw['y_range'] = sorted(set(ys))
    kw['title'] = "%s of %s" % (y_title, x_title)

    p = figure(x_axis_type ="datetime", plot_height=600, plot_width=800, tools='pan,box_zoom,reset', **kw)
    p.xaxis.axis_label = x_title
    p.yaxis.axis_label = y_title

    if x.value in discrete2:
        p.xaxis.major_label_orientation = pd.np.pi / 4

    sz = 0
    if size.value != 'None':
        sz = int(size.value)
        #groups = pd.qcut(df[size.value].values, len(SIZES))
        #sz = [SIZES[xx] for xx in groups.codes]

    if color.value == "Spectral":
        c = Spectral5[0]
        d = Spectral5[1]
        e = Spectral5[2]
        f = Spectral5[3]
    elif color.value == "RdYlBu":
        c = RdYlBu5[0]
        d = RdYlBu5[1]
        e = RdYlBu5[2]
        f = RdYlBu5[3]
    elif color.value == "Plasma":
        c = Plasma5[0]
        d = Plasma5[1]
        e = Plasma5[2]
        f = Plasma5[3]
    elif color.value == "Colorblind":
        c = Colorblind5[0]
        d = Colorblind5[1]
        e = Colorblind5[2]
        f = Colorblind5[3]
    else:   
        c = "#31AADE"
        d = "#de3154"
        e = "#debc31"
        f = "#31de65"
     
    if y.value =="Pressure Main and LoadLock":
        p.circle(x=xs, y=ys, color=c, size=sz, line_color="white", alpha=0.6, hover_color='white', hover_alpha=0.5)
        p.line(x=xs, y=ys, color=c, line_width=2, legend = "Pressure Main [mbar]")
        p.circle(x=xs, y=yb, color=d, size=sz, line_color="white", alpha=0.6, hover_color='white', hover_alpha=0.5)
        p.line(x=xs, y=yb, color=d, line_width=2, legend = "Pressure LoadLock [mbar]")
    elif y.value=="RoomTemp and Humidity":
        p.circle(x=xs, y=ys, color=c, size=sz, line_color="white", alpha=0.6, hover_color='white', hover_alpha=0.5)
        p.line(x=xs, y=ys, color=c, line_width=2, legend = "Room Temperature [degC]")
        p.circle(x=xs, y=yb, color=d, size=sz, line_color="white", alpha=0.6, hover_color='white', hover_alpha=0.5)
        p.line(x=xs, y=yb, color=d, line_width=2, legend = "Humidity [%]")
    elif y.value=='Chamber Temperature':
        p.circle(x=xs, y=ys, color=c, size=sz, line_color="white", alpha=0.6, hover_color='white', hover_alpha=0.5)
        p.line(x=xs, y=ys, color=c, line_width=2, legend = "Thermocouple 1 [degC]")
        p.circle(x=xs, y=yb, color=d, size=sz, line_color="white", alpha=0.6, hover_color='white', hover_alpha=0.5)
        p.line(x=xs, y=yb, color=d, line_width=2, legend = "Thermocouple 2 [degC]")
        p.circle(x=xs, y=yc, color=e, size=sz, line_color="white", alpha=0.6, hover_color='white', hover_alpha=0.5)
        p.line(x=xs, y=yc, color=e, line_width=2, legend = "Thermocouple 3 [degC]")
        p.circle(x=xs, y=yd, color=f, size=sz, line_color="white", alpha=0.6, hover_color='white', hover_alpha=0.5)
        p.line(x=xs, y=yd, color=f, line_width=2, legend = "Thermocouple 4 [degC]")   
    else:
        title = str(y_title)+" [mbar]"
        p.circle(x=xs, y=ys, color=c, size=sz, line_color="white", alpha=0.6, hover_color='white', hover_alpha=0.5)
        p.line(x=xs, y=ys, color =c, line_width=2, legend = title)
    p.legend.location = "top_left"
    return p


def update(attr, old, new):
    layout.children[1] = create_figure()


#x = Select(title='X-Axis', value='time', options=['time'])
x = Select(title='X-Axis', value="Last 24hrs", options=["Last 24hrs","Last 3 Days","Last Week","Last Month", "Last 3 Months","All Time"])
x.on_change('value', update)

y = Select(title='Y-Axis', value='Pressure Main and LoadLock', options=['Pressure Main','Pressure LoadLock', 'Pressure Main and LoadLock','RoomTemp and Humidity', 'Chamber Temperature'])
y.on_change('value', update)

size = Select(title='Size', value='None', options=['None','1','3','6','9','12','15','18'])
size.on_change('value', update)

color = Select(title='Color', value='None', options=['None','Spectral','RdYlBu','Plasma','Colorblind'])
color.on_change('value', update)

controls = widgetbox([x, y, color, size], width=250)
layout = row(controls, create_figure())

curdoc().add_root(layout)
curdoc().title = "DataLogger"
