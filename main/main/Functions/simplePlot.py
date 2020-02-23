import numpy as np
from bokeh.plotting import figure,gmap, output_file, save
from bokeh.models import ColumnDataSource, CustomJS, GMapOptions
from bokeh.models.widgets import RangeSlider, TextInput, CheckboxGroup, CheckboxButtonGroup
from bokeh.layouts import row, column
from bokeh.embed import components


def plot_map(cwd):
    map_options = GMapOptions(lat=30.2861, lng=-97.7394, map_type="roadmap", zoom=11)

    p = gmap("AIzaSyA5Cv2ZON6-Rx34LIUUVAJu3NdbPEMjpR8", map_options, title="Austin")
    source = ColumnDataSource(
        data=dict(lat=[ 30.29,  30.20,  30.29],
                  lon=[-97.70, -97.74, -97.78])
    )
    p.circle(x="lon", y="lat", size=15, fill_color="blue", fill_alpha=0.8, source=source)
    script, div = components(p)
    return script, div


def plot_data(cwd):
    file = np.loadtxt(cwd + '/main/Functions/TestFile.txt')
    last = 100
    data = dict(x=file[:, 0], y1=file[:, 1], y2=file[:, 2], y3=file[:, 3])
    raw_data = dict(x=file[:, 0], y1=file[:, 1], y2=file[:, 2], y3=file[:, 3])

    source = ColumnDataSource(data=data)
    raw_source = ColumnDataSource(data=raw_data)

    width = 600
    height = 400


    checkbox_group = CheckboxButtonGroup(labels=["a_x", "a_y", "a_z"], active=[0, 1, 2])
    range_slider = RangeSlider(start=0, end=file.shape[0], value=(0, file.shape[0]), step=1, title="Range1")
    text_start = TextInput(value="", title="Start:", width=100)
    text_end = TextInput(value="", title="End:", width=100)

    p = figure(title="a", plot_width=width, plot_height=height, tools = "pan,wheel_zoom,box_zoom,reset")
    l1 = p.line(x='x', y='y1', source=source, legend="a_x", line_color="red")
    l2 = p.line(x='x', y='y2', source=source, legend="a_y", line_color="blue")
    l3 = p.line(x='x', y='y3', source=source, legend="a_z", line_color="green")

    RangeSlider_callback = CustomJS(args=dict(
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
        const y2 = []
        const y3 = []
        const raw_x = raw_data['x']
        const raw_y1 = raw_data['y1']
        const raw_y2 = raw_data['y2']
        const raw_y3 = raw_data['y3']
        for (var i = 0; i < end - start; i++) {
            x[i] = raw_x[start + i]
            y1[i] = raw_y1[start + i]
            y2[i] = raw_y2[start + i]
            y3[i] = raw_y3[start + i]
        }
        source.data['x'] = x
        source.data['y1'] = y1
        source.data['y2'] = y2
        source.data['y3'] = y3
        source.change.emit();
    """)

    CheckboxGroup_callback = CustomJS(
                                    args=dict(
                                            checkbox_group=checkbox_group,
                                            l1=l1,
                                            l2=l2,
                                            l3=l3
                                            ),
                                    code="""
        active = checkbox_group.active

        l1.visible = active.includes(0);
        l2.visible = active.includes(1);
        l3.visible = active.includes(2);
    """)

    range_slider.js_on_change('value', RangeSlider_callback)
    checkbox_group.js_on_change('active', CheckboxGroup_callback)

    my_widgets = column(checkbox_group, row(text_start, text_end), range_slider)
    layout = column(my_widgets, p)
    script, div = components(layout)
    return script, div
