from bokeh.io import curdoc
from bokeh.transform import transform
from bokeh.models import ColumnDataSource, DatetimeTickFormatter,ResetTool,BoxZoomTool,PanTool, CategoricalColorMapper, HoverTool, WheelZoomTool
from bokeh.plotting import figure
from random import randrange
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from math import radians
import datetime
from pytz import timezone
import pandas as pd
from itertools import cycle
TOOLS = 'hover,pan,box_zoom,reset,wheel_zoom'
df = pd.read_csv('xrpusdt.csv')
df['closeTime2'] = pd.to_datetime(df['closeTime'],unit='ms')
str(df.closeTime2[0])
print(float(df.closeTime.values))
#nombre_csv = 'datos_crudos.csv'
#df = pd.read_csv(nombre_csv)

#create figure
f=figure(title= 'Precio XRP con velas de 1 minuto', y_axis_label = 'Precio (USDT)', height = 800, width=1200,
min_border_bottom = 0, y_range= (float(df.low.values) -.005, float(df.high.values) +.006 ),
#x_axis_type = 'datetime',
#x_range=(1632178919999,1632179919999)
tools = TOOLS)
f.title.text_color = 'olive'
f.title.text_alpha = 0.6
f.title.text_font = 'times'
f.title.text_font_size = '28px'
f.title.align = 'center'


f.yaxis.axis_label_text_font_size = "17pt"
f.xaxis.axis_label_text_font_size = "17pt"

f.yaxis.major_label_text_font_size = "11pt"
f.xaxis.major_label_text_font_size = "10pt"
f.xaxis.formatter=DatetimeTickFormatter(
milliseconds = ["%H:%M"],
seconds=["%H:%M"],
#minsec=["%Y-%m-%d-%H-%m-%S"],
minutes=["%H:%M"],
#hourmin=["%H:%M"],
hours=["%H:%M"],
days=["%H:%M"],
months=["%H:%M"],
years=["%H:%M"],
)


#create ColumnDataSource
data = {'x': df.closeTime2.values, 'y':df.close.values,
        'w':df.low.values, 'v':df.high.values, 'z':df.open.values, 't': ['dec' if (df['close'][0] < df['open'][0]) else 'inc']}

#data = {'x':[], 'y':[],
#        'w':[], 'v':[], 'z':[], 't':[]}
source=ColumnDataSource(data)
data
color_transform = transform('t',
                            CategoricalColorMapper(factors=['dec', 'inc'],
                                                   palette=['red', 'green']))



f.segment(x0='x', x1='x', y0='w', y1='v',
          color=color_transform, source=source)
# Using a segment instead of a vbar to set the width in pixels instead of X scale units.
f.segment(x0='x', x1='x', y0='z', y1='y',
          width=10, color=color_transform, source=source)

f.select_one(HoverTool).tooltips = [('Fecha','@x{%b-%d %l-%M}'), ('Close Price','@y'), ('Open Price','@z'),
 ('High Price','@v'), ('Low Price','@w')]

f.select_one(HoverTool).formatters = {'@x': 'datetime'}

#create periodic function
def update():
    df = pd.read_csv('C:\\Users\\Alfredo Zinzu\\Documents\\Codigo\\Bokeh\\velas\\xrpusdt.csv')
    #df['closeTime2'] = pd.to_datetime(df['closeTime'])

    new_data=dict(x=[pd.to_datetime(df['closeTime'][0],unit='ms')],y=[df.close],w=[df.low],v=[df.high],z=[df.open],t=['dec' if (df['close'][0] < df['open'][0]) else 'inc'])
    if new_data['z'] != source.data['z'][-1]:

        source.stream(new_data,rollover=30)
    #print(source.data)



f.xaxis.major_label_orientation=radians(60)

#add figure to curdoc and configure callback
curdoc().add_root(f)

#index_generator = cycle(range(len(df.index)))
#def stream():
#    df = pd.read_csv('datos_crudos.csv')
    #index = next(index_generator)
#    source.stream({'x': df.closeTime.values, 'y':df.closeXRPUSDT.values}, rollover = 20)
#curdoc().add_periodic_callback(stream, 10)


curdoc().add_periodic_callback(update,6000)


#esta es la versión que sólo plotea la serie de tiempo
