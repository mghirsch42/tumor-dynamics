import pandas as pd
from matplotlib import colormaps
from matplotlib import pyplot as plt
import seaborn as sns
from utils import get_id_colors

clone_growth_df = pd.read_csv("results/simple_model_2/clone_growth_rates.csv")
save_path = "figures/simple_model_2_ppt/obj_func/"
title_prefix = "Model 1"

clone_growth_df = clone_growth_df.sort_values(["exp", "id"])

save = True
show = True

id_colors = get_id_colors()

def plot_sep_by_exp(df, title, save_file, save, show):
    exps = df["exp"].unique()
    for i in range(len(exps)):
        exp_data = df[df["exp"]==exps[i]]
        for id in exp_data["id"].unique():
            plt.hist(exp_data[exp_data["id"]==id]["obj_func_val"], label=id, alpha=0.6, color=id_colors[id])
        plt.legend()
    plt.title(title)
    plt.xlabel("1-r^2")
    plt.ylabel("count")
    plt.tight_layout()
    if save:
        plt.savefig(save_file)
    if show:
        plt.show()
    plt.close()

for exp in clone_growth_df["exp"].unique():
    exp_df = clone_growth_df[clone_growth_df["exp"] == exp]
    plot_sep_by_exp(exp_df, title_prefix+"\n"+exp+"\nClone Growth Rates\nObjective Functions", save_path+exp+"clone_growth_rates_obj_func_ind.png", save, show)
