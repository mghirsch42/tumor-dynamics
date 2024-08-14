import numpy as np
from scipy.integrate import odeint
from sklearn.metrics import r2_score
import math
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def game(x, t, g1, g11):
    # Extract variables
    c1 = x[0]
    c11 = x[1]
    dxdt = [g1 * c1,
            g11 * c11]
    return dxdt

def run(init, g1, g11, true_df):
    max_time = true_df["last_day"].max()
    t = np.arange(0, max_time, 1)
    sol = odeint(game, init, t, args=(g1, g11))
    r2 = 0
    for idx, row in true_df.iterrows():
        true_curve = [np.exp(row["b"]*x+row["d"]) for x in t]
        r2 += r2_score(true_curve, sol[:,0]+sol[:,1])
        plt.plot(true_curve, color="black", label="true curve")
        plt.plot(sol[:,0]+sol[:,1], label="game estimated curve")
        plt.legend()
        plt.title(row["group"] + " " + str(row["id"]))
        plt.show()

    return r2/6

def get_init(group):
    if "B1" in group: return 1, 0
    if "B2" in group: return 0.8, 0.2
    if "B3" in group: return 0.5, 0.5
    if "B4" in group: return 0.2, 0.8
    if "B5" in group: return 0, 1

def main():
    save_path = "figures/jon/"
    # Define parameters
    group = "Grp. B1 nude (100% C1)"
    # group = "Grp. B2 nude (80% C1; 20% C11)"
    # group = "Grp. B3 nude (50% C1; 50% C11)"
    # group = "Grp. B4 nude (20% C1; 80% C11)"
    # group = "Grp. B5 nude (100% C11)"

    g1_range = [0.09, .18]
    g11_range = [0.09, .18]
    incr = 0.005
    c1_init, c11_init = get_init(group)
    c1_opt = 0.135
    c11_opt = 0.11
    c1_opt_loc = (c1_opt-g1_range[0])/incr-0.5  # The plot indices are based on the number
    c11_opt_loc = (c11_opt-g11_range[0])/incr+0.5   # of the box, not the value, y is indexed from bottom, x from top

    g1s = list(np.arange(g1_range[0], g1_range[1], incr))
    g11s = list(np.arange(g11_range[0], g11_range[1], incr))

    n_combos = len(g1s) * len(g11s)

    true_df = pd.read_csv("data/scaled_exbd_fit.csv")
    
    # Array of r2 scores for each combination of g1 and g11
    # Each row is [g1, g11, r2 score]
    r2_scores = np.zeros((n_combos, 3))

    # Loop through all combinations for g1 and g11 and get the r2 score
    for i in range(0, len(g1s)):
        for j in range(0, len(g11s)):
            score = run([c1_init, c11_init], g1s[i], g11s[j], true_df[true_df["group"] == group])
            r2_scores[i*len(g1s)+j] = [g1s[i], g11s[j], score]

    r2_df = pd.DataFrame(r2_scores, columns=["g1", "g11", "r2_score"])
    r2_df = pd.pivot(r2_df, index="g1", columns="g11", values="r2_score")
    r2_df.index = [round(r, 3) for r in r2_df.index]
    r2_df.columns = [round(c, 3) for c in r2_df.columns]
    r2_df = r2_df.sort_index(ascending=False)
    print(r2_df)
    plt.figure(figsize=(10,7))
    sns.heatmap(r2_df, cmap="hot", annot=False)
    # plt.axvline(x=c11_opt_loc)
    # plt.axhline(y=c1_opt_loc)
    plt.title(group)
    plt.ylabel("C1 growth rate")
    plt.xlabel("C11 growth rate")
    plt.tight_layout()
    # plt.savefig("{}heatmap{}_{}_{}_{}_{}_lines.png".format(save_path, group, g1_range[0], g1_range[1], g11_range[0], g11_range[1]))
    plt.savefig("{}heatmap{}_{}_{}_{}_{}.png".format(save_path, group, g1_range[0], g1_range[1], g11_range[0], g11_range[1]))
    plt.show()
main()