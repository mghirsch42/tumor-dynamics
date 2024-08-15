import numpy as np
from scipy.integrate import odeint, solve_ivp
from sklearn.metrics import r2_score
import math
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import warnings
import sys

def game(x, t, g1, g11, k, m):
    # Extract variables
    c1 = x[0]
    c11 = x[1]
    dxdt = [(g1 + k*c11) * c1,
            (g11 + m*c1) * c11]
    return dxdt

def run(init, g1, g11, k, m, true_df):
    max_time = true_df["last_day"].max()
    success = False
    while(success==False):
        with warnings.catch_warnings(record=True):
            t = np.arange(0, max_time, 1)
            sol = odeint(game, init, t, args=(g1, g11, k, m), full_output=True)
            if sol[1]["message"] == "Integration successful.": 
                success = True
                sol = sol[0]
            if max_time > 10:
                max_time = max_time -2
            else: return -sys.maxsize
    r2 = 0
    for idx, row in true_df.iterrows():
        true_curve = [np.exp(row["b"]*x+row["d"]) for x in t]
        r2 += r2_score(true_curve, sol[:,0]+sol[:,1])
        # plt.plot(true_curve, color="black", label="true curve")
        # plt.plot(sol[:,0]+sol[:,1], label="game estimated curve")
        # plt.legend()
        # plt.title(row["group"] + " " + str(row["id"]))
        # plt.show()

    return r2/len(true_df)

def get_init(group):
    if "A1" in group or "B1" in group: return 1, 0
    if "A2" in group or "B2" in group: return 0.8, 0.2
    if "A3" in group or "B3" in group: return 0.5, 0.5
    if "A4" in group or "B4" in group: return 0.2, 0.8
    if "A5" in group or "B5" in group: return 0, 1

def main():
    save_path = "figures/jon/"
    # Define parameters
    # group = "Grp. A1 B6 (100% C1)"
    group = "Grp. A2 B6 (80% C1; 20% C11)"
    # group = "Grp. A3 B6 (50% C1; 50% C11)"
    # group = "Grp. A4 B6 (20% C1; 80% C11)"
    # group = "Grp. A5 B6 (100% C11)"
    # group = "Grp. B1 nude (100% C1)"
    # group = "Grp. B2 nude (80% C1; 20% C11)"
    # group = "Grp. B3 nude (50% C1; 50% C11)"
    # group = "Grp. B4 nude (20% C1; 80% C11)"
    # group = "Grp. B5 nude (100% C11)"

    c1_init, c11_init = get_init(group)
    c1_opt = 0.02
    c11_opt = 0.078

    k_range = [-.8, .05] # C1 on C11
    m_range = [-1, .02] # C11 on C1
    incr = .05

    ks = list(np.arange(k_range[0], k_range[1], incr))
    ms = list(np.arange(m_range[0], m_range[1], incr))

    n_combos = len(ks) * len(ms)

    true_df = pd.read_csv("data/scaled_exbd_fit.csv")
    
    # Array of r2 scores for each combination of g1 and g11
    # Each row is [g1, g11, r2 score]
    r2_scores = np.zeros((n_combos, 3))

    # Loop through all combinations for g1 and g11 and get the r2 score
    for i in range(0, len(ks)):
        for j in range(0, len(ms)):
            score = run([c1_init, c11_init], c1_opt, c11_opt, ks[i], ms[j], true_df[true_df["group"] == group])
            r2_scores[i*len(ms)+j] = [ks[i], ms[j], score]

    r2_df = pd.DataFrame(r2_scores, columns=["k", "m", "r2_score"])
    r2_df = pd.pivot(r2_df, index="k", columns="m", values="r2_score")
    r2_df.index = [round(r, 3) for r in r2_df.index]
    r2_df.columns = [round(c, 3) for c in r2_df.columns]
    r2_df = r2_df.sort_index(ascending=False)
    print(r2_df)
    r2_df = r2_df.where(r2_df >= -10, -10) # Replace anything smaller than -x with -x
    plt.figure(figsize=(14,7.5))
    sns.heatmap(r2_df, cmap="hot", annot=True)
    # plt.axvline(x=c11_opt_loc)
    # plt.axhline(y=c1_opt_loc)
    plt.title(group)
    plt.ylabel("k: Influence of C11 on C1")
    plt.xlabel("m: Influence of C1 on C11")
    plt.tight_layout()
    # plt.savefig("{}heatmap{}_{}_{}_{}_{}_lines.png".format(save_path, group, g1_range[0], g1_range[1], g11_range[0], g11_range[1]))
    # plt.savefig("{}heatmap{}_{}_{}_{}_{}.png".format(save_path, group, g1_range[0], g1_range[1], g11_range[0], g11_range[1]))
    plt.savefig("{}heatmap_inter{}_{}_{}_{}_{}.png".format(save_path, group, k_range[0], k_range[1], m_range[0], m_range[1]))
    plt.show()
main()