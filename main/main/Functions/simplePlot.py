import numpy as np
from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models.widgets import RangeSlider
from bokeh.layouts import row, column
from bokeh.io import curdoc
from bokeh.embed import components


def plot_data(filename, cwd):
    output_file(cwd + "/templates/" + filename)

    file = np.loadtxt(cwd + '/main/Functions/TestFile.txt')
    last = 100
    data = dict(x=file[:, 0], y1=file[:, 1], y2=file[:, 2], y3=file[:, 3])
    raw_data = dict(x=file[:, 0], y1=file[:, 1], y2=file[:, 2], y3=file[:, 3])

    source = ColumnDataSource(data=data)
    raw_source = ColumnDataSource(data=raw_data)

    range_slider = RangeSlider(start=0, end=file.shape[0], value=(0, file.shape[0]), step=1, title="Range")

    p = figure(plot_width=800, plot_height=300)
    p.line(x='x', y='y1', source=source)

    callback = CustomJS(args=dict(raw_source=raw_source, source=source, range_slider=range_slider),
                        code="""
        const value = range_slider.value
        const start = value[0]
        const end = value[1]
        const raw_data = raw_source.data;
        const x = []
        const y1 = []
        const raw_x = raw_data['x']
        const raw_y1 = raw_data['y1']
        for (var i = 0; i < end - start; i++) {
            x[i] = raw_x[start + i]
            y1[i] = raw_y1[start + i]
        }
        source.data['x'] = x
        source.data['y1'] = y1
        source.change.emit();
    """)

    range_slider.js_on_change('value', callback)

    layout = row(range_slider, p)

    script, div = components(layout)
    return script, div
