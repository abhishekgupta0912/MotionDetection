from bokeh.models import HoverTool
from bokeh.plotting import figure, output_file, show

from src.script import df

p = figure(x_axis_type="datetime", height=200, width=700, title="Motion Graph")
p.yaxis.minor_tick_line_color = None

hover = HoverTool(tooltips=[("Start", "@START"), ("END", "@END")])
p.add_tools(hover)
p.quad(left=df["START"], right=df["END"], top=2, bottom=0)
output_file("Graph.html")

show(p)
