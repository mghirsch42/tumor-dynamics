import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from scipy.integrate import odeint
from sklearn.metrics import r2_score
import numpy as np
import warnings
import sys

def game(x, t, g1, g11, k, m):
    # Extract variables
    c1 = x[0]
    c11 = x[1]
    dxdt = [(g1 + k*c11) * c1,
            (g11 + m*c1) * c11]
    return dxdt

def get_init(group):
    if "A1" in group or "B1" in group: return 1, 0
    if "A2" in group or "B2" in group: return 0.8, 0.2
    if "A3" in group or "B3" in group: return 0.5, 0.5
    if "A4" in group or "B4" in group: return 0.2, 0.8
    if "A5" in group or "B5" in group: return 0, 1

true_df = pd.read_csv("data/scaled_exbd_fit.csv")
save_path = "figures/jon/"

# group = "Grp. A1 B6 (100% C1)"
# group = "Grp. A2 B6 (80% C1; 20% C11)"
# group = "Grp. A3 B6 (50% C1; 50% C11)"
# group = "Grp. A4 B6 (20% C1; 80% C11)"
group = "Grp. A5 B6 (100% C11)"
# group = "Grp. B1 nude (100% C1)"
# group = "Grp. B2 nude (80% C1; 20% C11)"
# group = "Grp. B3 nude (50% C1; 50% C11)"
# group = "Grp. B4 nude (20% C1; 80% C11)"
# group = "Grp. B5 nude (100% C11)"

# g1 = 0.135
# g11 = 0.11
# k = 0.7
# m = -1.0
g1 = 0.02
g11 = 0.078
k = -0.9
m = -0.2

c1_init, c11_init = get_init(group)

curr_df = true_df[true_df["group"] == group]

max_time = curr_df["last_day"].max()
success = False
while(success==False):
    with warnings.catch_warnings(record=True):
        t = np.arange(0, max_time, 1)
        sol = odeint(game, [c1_init, c11_init], t, args=(g1, g11, k, m), full_output=True)
        if sol[1]["message"] == "Integration successful.": 
            success = True
            sol = sol[0]
        if max_time > 10:
            max_time = max_time -2
        else:
            print("Couldn't solve.")
            exit()
r2 = 0
for idx, row in curr_df.iterrows():
    true_curve = [np.exp(row["b"]*x+row["d"]) for x in t]
    r2 += r2_score(true_curve, sol[:,0]+sol[:,1])
    plt.figure()
    plt.plot(true_curve, color="black", label="true curve")
    plt.plot(sol[:,0], label="game estimated C1", linewidth=6, alpha=0.5)
    plt.plot(sol[:,1], label="game estimated C11", linewidth=6, alpha=0.5)
    plt.plot(sol[:,0]+sol[:,1], label="game estimated curve", color="red")
    plt.legend()
    plt.title(row["group"] + " " + str(row["id"]))
    plt.tight_layout()
    plt.savefig(save_path + "inter_" + row["group"] + "_" + str(row["id"]) + ".png")
    plt.show()
    plt.close()

