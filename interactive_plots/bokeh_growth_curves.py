import numpy as np
from bokeh.layouts import column, row, layout
from bokeh.models import ColumnDataSource, CustomJS, Slider, Range1d
from bokeh.plotting import figure, show
from bokeh.io import output_notebook
from scipy.integrate import odeint
import pandas as pd

#####
# Use Bokeh to plot growth curves for 100% mice with sliders for growth rates.
# Plots the true growth curves for those mice as comparison.
# Will create an HTML file with the interactive plots.
#####

def get_init(group):
    if "A1" in group or "B1" in group: return 1, 0
    if "A2" in group or "B2" in group: return 0.8, 0.2
    if "A3" in group or "B3" in group: return 0.5, 0.5
    if "A4" in group or "B4" in group: return 0.2, 0.8
    if "A5" in group or "B5" in group: return 0, 1

def game(x, t, g1, g11):
    c1 = x[0]
    c11 = x[1]
    dxdt = [g1 * c1,
            g11 * c11]
    return dxdt

true_df = pd.read_csv("data/scaled_exbd_fit.csv")

groups = ["Grp. A1 B6 (100% C1)", "Grp. A5 B6 (100% C11)", "Grp. B1 nude (100% C1)", "Grp. B5 nude (100% C11)"]
g1 = 0
g11 = 0

sources = []
for g in range(len(groups)):
    c1_init, c11_init = get_init(groups[g])
    max_time = true_df[true_df["group"]==groups[g]]["last_day"].max()
    x = np.arange(0, max_time, 1)
    sol = odeint(game, [c1_init, c11_init], x, args=(g1, g11))
    y = sol[:,0]
    z = sol[:,1]
    sources.append(ColumnDataSource(data=dict(x=x, y=y, z=z)))

plots = []
for g in range(len(groups)):
    # Create figure
    p = figure(title=groups[g], width=500, height=300)
    # Plot true curves and get plot bounds
    x_max = 0
    y_max = 0
    curr_df = true_df[true_df["group"]==groups[g]]
    for idx, df_row in curr_df.iterrows():
        t = np.arange(0, df_row["last_day"], 1)
        true_curve = [np.exp(df_row["b"]*x+df_row["d"]) for x in t]
        if t[-1] > x_max: x_max = t[-1]
        if max(true_curve) > y_max: y_max = max(true_curve)
        p.line(x = t, y=true_curve, line_color="black", legend_label="true curves")
    # Plot game estimated curves
    p.line("x", "y", source=sources[g], line_width=3, line_color="orange", line_alpha=0.6, legend_label="C1")
    p.line("x", "z", source=sources[g], line_width=3, line_color="blue", line_alpha=0.6, legend_label="C11")
    # Annotations
    p.x_range = Range1d(-1, x_max+1)
    p.y_range = Range1d(-1, y_max+1)
    p.legend.location="top_left"
    plots.append(p)

g1_slider = Slider(start=0, end=0.2, value=g1, step=.01, title="G1 Growth Rate")
g11_slider = Slider(start=0, end=0.2, value=g11, step=.01, title="G11 Growth Rate")

callback = CustomJS(args=dict(sources=sources, g1_slider=g1_slider, g11_slider=g11_slider),
                    code="""
    const a = g1_slider.value
    const b = g11_slider.value
    
    var game = function(t, c1, c11, g1, g11) {
        const c1_result = [c1]
        const c11_result = [c11]
        for (let i=1; i<t.length; i++) {
            const dt = t[i] - t[i-1]
            c1 += g1*c1*dt
            c11 += g11*c11*dt
            c1_result.push(c1)
            c11_result.push(c11)
        }
        return [c1_result, c11_result]
    }

    for (let i=0; i<sources.length; i++) {
        let x = sources[i].data.x
        let res = game(x, sources[i].data.y[0], sources[i].data.z[0], a, b)
        let y = res[0]
        let z = res[1]
        sources[i].data = {x, y, z}
    }
""")
g1_slider.js_on_change("value", callback)
g11_slider.js_on_change("value", callback)

show(layout([plots[0:2], plots[2:4], [g1_slider, g11_slider]]))