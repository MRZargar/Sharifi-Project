import numpy as np
from bokeh.plotting import figure, output_file, save
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models.widgets import RangeSlider, TextInput
from bokeh.layouts import row, column
from bokeh.io import curdoc
from bokeh.embed import components


def create_callback(raw_source, source, range_slider, string):
    callback = CustomJS(args=dict(
                                raw_source=raw_source,
                                source=source,
                                range_slider=range_slider,
                                ),
                        code="""
        const value = range_slider.value
        const start = value[0]
        const end = value[1]
        const raw_data = raw_source.data;
        const x = []
        const y1 = []
        const raw_x = raw_data['x']
        const raw_{0} = raw_data['{0}']
        for (var i = 0; i < end - start; i++) {
            x[i] = raw_x[start + i]
            {0}[i] = raw_{0}[start + i]
        }
        source.data['x'] = x
        source.data['{0}'] = {0}
        source.change.emit();
    """)
    return callback


def plot_data(filename, cwd):
    output_file(cwd + "/templates/" + filename)

    file = np.loadtxt(cwd + '/main/Functions/TestFile.txt')
    last = 100
    data = dict(x=file[:, 0], y1=file[:, 1], y2=file[:, 2], y3=file[:, 3])
    raw_data = dict(x=file[:, 0], y1=file[:, 1], y2=file[:, 2], y3=file[:, 3])

    source = ColumnDataSource(data=data)
    raw_source = ColumnDataSource(data=raw_data)

    width = 800
    height = 200

    range_slider1 = RangeSlider(start=0, end=file.shape[0], value=(0, file.shape[0]), step=1, title="Range")
    text_start1 = TextInput(value="", title="Start:", width=100)
    text_end1 = TextInput(value="", title="End:", width=100)
    p1 = figure(title="a_x", plot_width=width, plot_height=height)
    p1.line(x='x', y='y1', source=source)
    callback1 = create_callback(raw_source, source, range_slider1, 'y1')
    range_slider1.js_on_change('value', callback1)

    range_slider2 = RangeSlider(start=0, end=file.shape[0], value=(0, file.shape[0]), step=1, title="Range")
    text_start2 = TextInput(value="", title="Start:", width=100)
    text_end2 = TextInput(value="", title="End:", width=100)
    p2 = figure(title="a_y", plot_width=width, plot_height=height)
    p2.line(x='x', y='y2', source=source)
    callback2 = create_callback(raw_source, source, range_slider2, 'y2')
    range_slider2.js_on_change('value', callback2)

    range_slider3 = RangeSlider(start=0, end=file.shape[0], value=(0, file.shape[0]), step=1, title="Range")
    text_start3 = TextInput(value="", title="Start:", width=100)
    text_end3 = TextInput(value="", title="End:", width=100)
    p3 = figure(title="a_z", plot_width=width, plot_height=height)
    p3.line(x='x', y='y3', source=source)
    callback3 = create_callback(raw_source, source, range_slider3, 'y3')
    range_slider3.js_on_change('value', callback3)

    layout1 = row(column(row(text_start1, text_end1), range_slider1), p1)
    layout2 = row(column(row(text_start2, text_end2), range_slider2), p2)
    layout3 = row(column(row(text_start3, text_end3), range_slider3), p3)
    layout = column(layout1, layout2, layout3)

    script, div = components(layout)
    return script, div
