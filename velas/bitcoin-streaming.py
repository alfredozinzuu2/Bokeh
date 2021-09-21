from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, DatetimeTickFormatter
from bokeh.plotting import figure
from random import randrange
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from math import radians
from pytz import timezone
import pandas as pd
from itertools import cycle

df = pd.read_csv('xrpusdt.csv')
df
#nombre_csv = 'datos_crudos.csv'
#df = pd.read_csv(nombre_csv)
#create figure
f=figure(title= 'Precio XRP con velas de 1 minuto',x_axis_label='Fechas', y_axis_label = 'Precio (USDT)', height = 800, width=1200,
min_border_bottom = -800)
f.title.text_color = 'olive'
f.title.text_alpha = 0.6
f.title.text_font = 'times'
f.title.text_font_size = '28px'
f.title.align = 'center'


f.yaxis.axis_label_text_font_size = "17pt"
f.xaxis.axis_label_text_font_size = "17pt"

f.yaxis.major_label_text_font_size = "11pt"
f.xaxis.major_label_text_font_size = "10pt"

#create webscraping function
def extract_value():
    r=requests.get("http://bitcoincharts.com/markets/btcnCNY.html",headers={'User-Agent':'Mozilla/5.0'})
    c=r.content
    soup=BeautifulSoup(c,"html.parser")
    value_raw=soup.find_all("p")
    value_net=float(value_raw[0].span.text)
    return value_net

#create ColumnDataSource
data = {'x': df.closeTime.values, 'y':df.close.values}
source=ColumnDataSource(data)
data
#create glyphs
f.circle(x='x',y='y',color='olive',line_color='brown',source=source)
f.line(x='x',y='y',source=source)

#create periodic function
def update():
    df = pd.read_csv('C:\\Users\\Alfredo Zinzu\\Documents\\Codigo\\Bokeh\\velas\\xrpusdt.csv')
    new_data=dict(x=[df.closeTime],y=[df.close])
    source.stream(new_data,rollover=3000)
    #print(source.data)
f.xaxis.formatter=DatetimeTickFormatter(
#seconds=["%Y-%m-%d-%H-%m-%S"],
#minsec=["%Y-%m-%d-%H-%m-%S"],
minutes=["%Y-%m-%d-%H-%m-%S"],
#hourmin=["%Y-%m-%d-%H-%m-%S"],
hours=["%Y-%m-%d-%H-%m-%S"],
days=["%Y-%m-%d-%H-%m-%S"],
#months=["%Y-%m-%d-%H-%m-%S"],
#years=["%Y-%m-%d-%H-%m-%S"],
)


f.xaxis.major_label_orientation=radians(0)

#add figure to curdoc and configure callback
curdoc().add_root(f)

#index_generator = cycle(range(len(df.index)))
#def stream():
#    df = pd.read_csv('datos_crudos.csv')
    #index = next(index_generator)
#    source.stream({'x': df.closeTime.values, 'y':df.closeXRPUSDT.values}, rollover = 20)
#curdoc().add_periodic_callback(stream, 10)


curdoc().add_periodic_callback(update,40000)
