import numpy as np
from bokeh.layouts import column, row, layout
from bokeh.models import ColumnDataSource, CustomJS, Slider, Range1d
from bokeh.plotting import figure, show
from bokeh.io import output_notebook
from scipy.integrate import solve_ivp
import pandas as pd

#####
# Use Bokeh to plot growth curves for admixture mice with sliders for growth rates and interaction terms.
# Plots the true growth curves for those mice as comparison.
# Will create an HTML file with the interactive plots.
#####

def get_init(group):
    if "A1" in group or "B1" in group: return 1, 0
    if "A2" in group or "B2" in group: return 0.8, 0.2
    if "A3" in group or "B3" in group: return 0.5, 0.5
    if "A4" in group or "B4" in group: return 0.2, 0.8
    if "A5" in group or "B5" in group: return 0, 1

def game(t, x, g1, g11, k, m):
    c1 = x[0]
    c11 = x[1]
    dxdt = [(g1 + k*c11) * c1,
            (g11 + m*c1) * c11]
    return dxdt

true_df = pd.read_csv("data/scaled_exbd_fit.csv")

groups = ["Grp. A2 B6 (80% C1; 20% C11)", "Grp. A3 B6 (50% C1; 50% C11)", "Grp. A4 B6 (20% C1; 80% C11)", "Grp. B2 nude (80% C1; 20% C11)", "Grp. B3 nude (50% C1; 50% C11)", "Grp. B4 nude (20% C1; 80% C11)"]
# g1 = 0.135
# g11 = 0.11
g1 = .1
g11 = 0
k = 0 # K is influence of C11 on C1
m = 0 # M is influence of C1 on C11

sources = []
for g in range(len(groups)):
    c1_init, c11_init = get_init(groups[g])
    max_time = true_df[true_df["group"]==groups[g]]["last_day"].max()
    x = np.arange(0, max_time, 1)
    sol = solve_ivp(game, (0,max_time), [c1_init, c11_init], args=(g1, g11, k, m), t_eval=x)
    sol = sol.y
    # print(sol)
    y = sol[0]
    z = sol[1]
    sources.append(ColumnDataSource(data=dict(x=x, y=y, z=z)))

print(sources[0].data)

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
k_slider = Slider(start=-0.5, end=0.5, value=k, step=.01, title="k (C11 on C1")
m_slider = Slider(start=-0.5, end=0.5, value=m, step=.01, title="m (C1 on C11)")

callback = CustomJS(args=dict(sources=sources, g1_slider=g1_slider, g11_slider=g11_slider, k_slider=k_slider, m_slider=m_slider),
                    code="""
    var game = function(t, c1, c11, g1, g11, k, m) {
        console.log(g1)
        console.log(g11)
        const c1_result = [c1]
        const c11_result = [c11]
        for (let i=1; i<t.length; i++) {
            const dt = t[i] - t[i-1]
            c1 += (g1+k*c11)*c1
            c11+= (g11+m*c1)*c11
            c1_result.push(c1)
            c11_result.push(c11)
        }
        return [c1_result, c11_result]
    }

    console.log(sources[0].data)
    for (let i=0; i<sources.length; i++) {
        let x = sources[i].data.x
        let res = game(x, sources[i].data.y[0], sources[i].data.z[0], g1_slider.value, g11_slider.value, k_slider.value, m_slider.value)
        let y = res[0]
        let z = res[1]
        
        sources[i].data = {x, y, z}
    }
""")
g1_slider.js_on_change("value", callback)
g11_slider.js_on_change("value", callback)
k_slider.js_on_change("value", callback)
m_slider.js_on_change("value", callback)

show(layout(
    [
        plots[0:3], 
        plots[3:6], 
        [g1_slider, g11_slider, k_slider, m_slider]
    ]))