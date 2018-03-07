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

data.columns =["time","main","prep","roomtemp","humidity",'t1','t2','t3','t4']
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

    if y.value =="main and prep":
        ys = data['main'].values
        yb = data['prep'].values
    else:
        ys = data[y.value].values
        yb = np.zeros(len(xs))
    x_title = x.value.title()
    y_title = y.value.title()
    now = datetime.datetime.now()   
    if x.value == "Last 24hrs":
        val= 0
        index =0
        for element in data["time"]:
            a = now-element
            if datetime.timedelta(127.0125) >= a:
                val = index
                break
            index +=1
        xs = xs[val:]
        ys = ys[val:]
        yb = yb[val:]
    if x.value == "Last 3 Days":
        val= 0
        index = 0
        for element in data["time"]:
            a = now-element
            if datetime.timedelta(129.0125) >= a:
                val = index
                break
            index +=1
        xs = xs[val:]
        ys = ys[val:]
        yb = yb[val:]
    if x.value == "Last Week":
        val= 0
        index = 0
        for element in data["time"]:
            a = now-element
            if datetime.timedelta(130.0125) >= a:
                val = index
                break
            index +=1
        xs = xs[val:]
        ys = ys[val:]
        yb = yb[val:]
    if x.value == "All Time" :
        xs = xs
        ys = ys
        yb = yb
    kw = dict()
    if x.value in discrete2:
        kw['x_range'] = sorted(set(xs))
    if y.value in discrete2:
        kw['y_range'] = sorted(set(ys))
    kw['title'] = "%s of %s" % (y_title, x_title)

    p = figure(x_axis_type ="datetime", plot_height=780, plot_width=1040, tools='pan,box_zoom,reset', **kw)
    p.xaxis.axis_label = x_title
    p.yaxis.axis_label = y_title

    if x.value in discrete2:
        p.xaxis.major_label_orientation = pd.np.pi / 4

    sz = 9
    if size.value != 'None':
        sz = int(size.value)
        #groups = pd.qcut(df[size.value].values, len(SIZES))
        #sz = [SIZES[xx] for xx in groups.codes]
    if color.value == "None":   
        c = "#31AADE"
        d = "#de3154"
    if color.value == "Spectral":
        c = Spectral5[0]
        d = Spectral5[1]
    if color.value == "RdYlBu":
        c = RdYlBu5[0]
        d = RdYlBu5[1]
    if color.value == "Plasma":
        c = Plasma5[0]
        d = Plasma5[1]
    if color.value == "Colorblind":
        c = Colorblind5[0]
        d = Colorblind5[1]

     
    if y.value =="main and prep":
        p.circle(x=xs, y=ys, color=c, size=sz, line_color="white", alpha=0.6, hover_color='white', hover_alpha=0.5)
        p.line(x=xs, y=ys, color=c, line_width=2)
        p.circle(x=xs, y=yb, color=d, size=sz, line_color="white", alpha=0.6, hover_color='white', hover_alpha=0.5)
        p.line(x=xs, y=yb, color=d, line_width=2)
        
    else:    
        p.circle(x=xs, y=ys, color=c, size=sz, line_color="white", alpha=0.6, hover_color='white', hover_alpha=0.5)
        p.line(x=xs, y=ys, line_width=2)

    return p


def update(attr, old, new):
    layout.children[1] = create_figure()


#x = Select(title='X-Axis', value='time', options=['time'])
x = Select(title='X-Axis', value="Last 24hrs", options=["Last 24hrs","Last 3 Days","Last Week","All Time"])
x.on_change('value', update)

y = Select(title='Y-Axis', value='main', options=['main','prep', 'main and prep'])
y.on_change('value', update)

size = Select(title='Size', value='None', options=['None','1','3','6','9','12','15','18'])
size.on_change('value', update)

color = Select(title='Color', value='None', options=['None','Spectral','RdYlBu','Plasma','Colorblind'])
color.on_change('value', update)

controls = widgetbox([x, y, color, size], width=200)
layout = row(controls, create_figure())

curdoc().add_root(layout)
curdoc().title = "Crossfilter"