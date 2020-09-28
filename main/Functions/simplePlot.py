import numpy as np
from bokeh.plotting import figure,gmap, output_file, save
from bokeh.models import ColumnDataSource, CustomJS, GMapOptions, HoverTool, OpenURL, TapTool, PrintfTickFormatter
from bokeh.models.widgets import RangeSlider, TextInput, CheckboxGroup, CheckboxButtonGroup
from bokeh.layouts import row, column
from bokeh.embed import components
from bokeh.tile_providers import CARTODBPOSITRON, get_provider
import math


def merc_x(lon):
  r_major=6378137.000
  return r_major*math.radians(lon)


def merc_y(lat):
  if lat>89.5:lat=89.5
  if lat<-89.5:lat=-89.5
  r_major=6378137.000
  r_minor=6356752.3142
  temp=r_minor/r_major
  eccent=math.sqrt(1-temp**2)
  phi=math.radians(lat)
  sinphi=math.sin(phi)
  con=eccent*sinphi
  com=eccent/2
  con=((1.0-con)/(1.0+con))**com
  ts=math.tan((math.pi/2-phi)/2)/con
  y=0-r_major*math.log(ts)
  return y


def plot_map(cwd):
    sizing_mode = 'scale_width'
    tile_provider = get_provider(CARTODBPOSITRON)
    p = figure(x_range=(merc_x(40), merc_x(65)), y_range=(merc_y(20), merc_y(45)),
            x_axis_type="mercator", y_axis_type="mercator",
            tools="pan,wheel_zoom,box_zoom,reset,tap",
            sizing_mode=sizing_mode
            )
    p.add_tile(tile_provider)

    source = ColumnDataSource(
        data=dict(lat=[33, 25, 35],
                  lon=[49, 60, 54],
                  merc_lon = list(map(merc_x, [49, 60, 54])),
                  merc_lat = list(map(merc_y, [33, 25, 35])),
                  name=['St1', 'St2', 'St3'],)
    )
    p.circle(x="merc_lon", y="merc_lat", size=15, fill_color="blue", fill_alpha=0.8, source=source)
    p.add_tools(HoverTool(
        tooltips=[
            ( 'name',   '@name'            ),
            ( '(lat, lon)',  '(@lat, @lon)' ),
        ],
    ))

    url = "http://127.0.0.1:8000/plot"
    taptool = p.select(type=TapTool)
    taptool.callback = OpenURL(url=url)

    script, div = components(p)
    return script, div


def plot_data(cwd):
    file = np.loadtxt(cwd + '/main/Functions/Obs.txt', skiprows=2)
    last = 100
    data = dict(x=file[:, 0], y1=file[:, 1], y2=file[:, 2], y3=file[:, 3])
    raw_data = dict(x=file[:, 0], y1=file[:, 1], y2=file[:, 2], y3=file[:, 3])

    source = ColumnDataSource(data=data)
    raw_source = ColumnDataSource(data=raw_data)

    width = 800
    height = 400

    sizing_mode = 'scale_width'

    checkbox_group = CheckboxButtonGroup(labels=["a_x", "a_y", "a_z"], active=[0, 1, 2], sizing_mode=sizing_mode)
    range_slider = RangeSlider(start=0, end=file.shape[0], width=600, height=100, value=(0, file.shape[0]), step=1, title="Range1", sizing_mode=sizing_mode)
    text_start = TextInput(value="0", title="Start:", width=100, height=50, sizing_mode=sizing_mode)
    text_end = TextInput(value=str(len(data['x'])), title="End:", width=100, height=50, sizing_mode=sizing_mode)

    # p = figure(title="a", plot_width=width, plot_height=height, tools = "pan,wheel_zoom,box_zoom,reset")
    # l1 = p.line(x='x', y='y1', source=source, legend_label="a_x", line_color="red")
    # l2 = p.line(x='x', y='y2', source=source, legend_label="a_y", line_color="blue")
    # l3 = p.line(x='x', y='y3', source=source, legend_label="a_z", line_color="green")
    #  plot_width=width, plot_height=height,

    axis_label_text_font_size = '20pt'

    p1 = figure(title="", plot_width=width, plot_height=height, tools="reset,pan,wheel_zoom,box_zoom", sizing_mode=sizing_mode, toolbar_location="below")
    l1 = p1.line(x='x', y='y1', source=source, line_color="red")
    p1.yaxis.axis_label = 'a_x'
    p1.xaxis.axis_label_text_font_size = axis_label_text_font_size
    p1.yaxis.axis_label_text_font_size = axis_label_text_font_size
    p2 = figure(title="", plot_width=width, plot_height=height, tools="reset,pan,wheel_zoom,box_zoom", sizing_mode=sizing_mode, toolbar_location="below")
    l2 = p2.line(x='x', y='y2', source=source, line_color="blue")
    p2.yaxis.axis_label = 'a_y'
    p2.xaxis.axis_label_text_font_size = axis_label_text_font_size
    p2.yaxis.axis_label_text_font_size = axis_label_text_font_size
    p3 = figure(title="", plot_width=width, plot_height=height, tools="reset,pan,wheel_zoom,box_zoom", sizing_mode=sizing_mode, toolbar_location="below")
    l3 = p3.line(x='x', y='y3', source=source, line_color="green")
    p3.yaxis.axis_label = 'a_z'
    p3.xaxis.axis_label_text_font_size = axis_label_text_font_size
    p3.yaxis.axis_label_text_font_size = axis_label_text_font_size

    xaxis_format = PrintfTickFormatter(format="%i")
    yaxis_format = PrintfTickFormatter(format="%5.1e")

    p1.xaxis[0].formatter = xaxis_format
    p1.yaxis[0].formatter = yaxis_format
    p2.xaxis[0].formatter = xaxis_format
    p2.yaxis[0].formatter = yaxis_format
    p3.xaxis[0].formatter = xaxis_format
    p3.yaxis[0].formatter = yaxis_format

    p1.yaxis.minor_tick_line_color = None
    p2.yaxis.minor_tick_line_color = None
    p3.yaxis.minor_tick_line_color = None
    p1.xaxis.minor_tick_line_color = None
    p2.xaxis.minor_tick_line_color = None
    p3.xaxis.minor_tick_line_color = None


    p1.yaxis.axis_label_text_font_size = "15px"
    p2.yaxis.axis_label_text_font_size = "15px"
    p3.yaxis.axis_label_text_font_size = "15px"

    p1.xaxis.major_label_text_font_size = "13px"
    p2.xaxis.major_label_text_font_size = "13px"
    p3.xaxis.major_label_text_font_size = "13px"


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

    text_start_end_callback = CustomJS(args=dict(
                                raw_source=raw_source,
                                source=source,
                                range_slider=range_slider,
                                text_start=text_start,
                                text_end=text_end
                                ),
                        code="""
        const new_value = []
        new_value[0] = parseInt(text_start.value)
        new_value[1] = parseInt(text_end.value)
        range_slider.value = new_value
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
    text_end.js_on_change('value', text_start_end_callback)
    text_start.js_on_change('value', text_start_end_callback)

    my_widgets = row(text_start, text_end)
    my_widgets.sizing_mode = 'fixed'
    layout = column(my_widgets, range_slider, p1, p2, p3)
    layout.sizing_mode = sizing_mode

    script, div = components(layout)
    return script, div
