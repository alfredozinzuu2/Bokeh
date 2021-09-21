                #"""Importamos las librerías necesarias"""

from bokeh.io import curdoc, output_file, show, save
from bokeh.models import ColumnDataSource, DatetimeTickFormatter, CategoricalColorMapper
from bokeh.plotting import figure
from bokeh.transform import transform
import pandas as pd

nombre_del_csv = 'ethusdt.csv'
df = pd.read_csv('xrpusdt.csv')
                #"""Creamos nuestra figura para poder graficar"""


#f = figure(x.axis_type = 'datetime'
#            x.axis_label='Fecha', y.axis_label='USD')
                                                        #Configuramos nuestro eje, puesto que los valores van a ser datetimes

output_file('plot.html')
f = figure()

                #"""Ahora definimos la columna de donde vamos a extraer nuestros datos"""

inc_color = 'green'
dec_color = 'red'
#source = ColumnDataSource(dict(datetime = [], close = []))
source = ColumnDataSource(dict(datetime = [], low = [], high = [], open = [], close = [], trend = []))
color_transform = transform('trend', CategoricalColorMapper(factors=['dec','inc'], palette=['red','green']))


                #"""Creamos las viñetas para ir graficando los puntos"""

#f.circle(x = 'x', y = 'y', color = 'olive', line_color = 'brown', source = source)
#f.line(x = 'x', y = 'y', line_color = 'green', source = source)

f.segment(x0='datetime', x1='datetime', y0='low', y1='high',
          color=color_transform, source=source)
# Using a segment instead of a vbar to set the width in pixels instead of X scale units.
f.segment(x0='datetime', x1='datetime', y0='open', y1='close',
          line_width=10, color=color_transform, source=source)


                #"""Necesitamos una función que vaya renovando los datos para la graficación"""

#def update_data_plot():
#    new_data = dict(x=[datetime.now()], y=[valores de y])
#    source.stream(new_data, rollover = 200)

def update_data_plot():
    source.stream(dict(datetime=[df.closeTime], open=[df.open], close=[df.close],
                   low=[df.low], high=[df.high],
                   trend=['dec' if df.close < df.open else 'inc']),
                   rollover=10)


                #"""Necesitamos que aparezcan las fechas, el timestamp, entonces le damos formato al datetimes"""

f.xaxis.formatter = DatetimeTickFormatter(
seconds=['%Y-%m-%d-%H-%M-%S'],
minutes=['%Y-%m-%d-%H-%M-%S'],
hours=['%Y-%m-%d-%H-%M-%S'],
days=['%Y-%m-%d-%H-%M-%S'],
months=['%Y-%m-%d-%H-%M-%S'],
years=['%Y-%m-%d-%H-%M-%S'],
)

curdoc().add_root(f)
curdoc().add_periodic_callback(update_data_plot,5000)


save(f)
#show(f)
