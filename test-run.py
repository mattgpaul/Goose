
#%% Imports

from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, DatetimeTickFormatter, Select
from bokeh.layouts import layout
from bokeh.plotting import figure
from datetime import datetime
from math import radians
import psutil

#%% Create Figure
TOOLTIPS = [
    ('(x,y)','($x,$y)')
]
p = figure(x_axis_type='datetime', width=1800, height=1000, tooltips=TOOLTIPS)

#%% Generate Data

def create_value():
    walk = psutil.cpu_percent()
    return walk

#%% Create Data Source

source = ColumnDataSource(dict(x=[], y=[]))
p.circle(x='x',y='y', color='firebrick', line_color='firebrick', source=source)
p.line(x='x', y='y', source=source)

#%% Create Periodic Callback Function

def update():
    new_data = dict(
        x=[datetime.now()],
        y=[create_value()]
    )
    source.stream(new_data, rollover=200)
    p.title.text='Now Streaming %s Data' % select.value
    
def update_intermed(attrname, old, new):
    source.data=dict(x=[], y=[])
    update()


#%% Formatting axis

date_pattern = ['%Y-%m-%d\n%H:%M:%S']
p.xaxis.formatter = DatetimeTickFormatter(
    seconds=date_pattern,
    minsec=date_pattern,
    minutes=date_pattern,
    hourmin=date_pattern,
    hours=date_pattern,
    days=date_pattern,
    months=date_pattern,
    years=date_pattern
)

p.xaxis.major_label_orientation=radians(80)
p.xaxis.axis_label='Date'
p.yaxis.axis_label='Value'

#%% Create Selection Widget

options = [('stock1', 'Stock One'), ('stock2','Stock Two')]
select = Select(title='Market Name', value='stock1', options=options)
select.on_change('value', update_intermed)

#%% Configure Layout

lay_out = layout([[p], [select]])
curdoc().title = 'Streaming Stock Data Example'
curdoc().add_root(lay_out)
curdoc().add_periodic_callback(update, 500)
