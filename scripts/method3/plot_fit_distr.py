import pandas as pd
from matplotlib import colormaps
from matplotlib import pyplot as plt
import seaborn as sns
from utils import get_group_colors, get_id_colors

clone_growth_df = pd.read_csv("results/method3/clone_growth_rates.csv")
clone_intr_df = pd.read_csv("results/method3/clone_interaction.csv")
t_intr_pure_df = pd.read_csv("results/method3/t_interaction_pure.csv")
t_intr_admix_df = pd.read_csv("results/method3/t_interaction.csv")
save_path = "figures/method3/"
title_prefix = "Method 3"

clone_growth_df = clone_growth_df.sort_values(["exp", "id"])
clone_intr_df = clone_intr_df.sort_values(["exp", "id"])
t_intr_pure_df = t_intr_pure_df.sort_values(["exp", "id"])
t_intr_admix_df = t_intr_admix_df[(t_intr_admix_df["exp"] != "Grp. A1 B6 (100% C1)") & (t_intr_admix_df["exp"] != "Grp. A5 B6 (100% C11)")]
t_intr_admix_df = t_intr_admix_df.sort_values(["exp", "id"])

save = True
show = True

group_colors = get_group_colors()
id_colors = get_id_colors()

def plot_sep_by_exp(df, title, save_file, save, show):
    exps = df["exp"].unique()
    fig, axes = plt.subplots(nrows=1, ncols=len(exps), figsize=(14,7))
    for i in range(len(exps)):
        exp_data = df[df["exp"]==exps[i]]
        for id in exp_data["id"].unique():
            axes[i].hist(exp_data[exp_data["id"]==id]["obj_func_val"], label=id, alpha=0.6, color=id_colors[id])
        axes[i].set(xlabel="", ylabel="")
        axes[i].set_title(exps[i])
        axes[i].legend()
    plt.suptitle(title)
    fig.supxlabel("1-r^2")
    fig.supylabel("count")
    plt.tight_layout()
    if save:
        plt.savefig(save_file)
    if show:
        plt.show()
    plt.close()

def plot_all_on_one(df, title, save_file, save, show):
    plt.figure()
    for exp in df["exp"].unique():
        plt.hist(df[df["exp"] == exp]["obj_func_val"], label=exp, alpha=0.6, color=group_colors[exp])
    plt.legend()
    plt.xlabel("1-r^2")
    plt.ylabel("count")
    plt.title(title)
    if save:
        plt.savefig(save_file)
    if show:
        plt.show()
    plt.close()


def plot_fit_vs_value_by_exp(df, var, title, save_file, save, show):
    exps = df["exp"].unique()
    fig, axes = plt.subplots(nrows=1, ncols=len(exps), figsize=(14,7))
    if type(axes) == plt.Axes: axes = [axes]
    for i in range(len(exps)):
        exp_data = df[df["exp"]==exps[i]]
        for id in exp_data["id"].unique():
            axes[i].scatter(x=exp_data[exp_data["id"]==id]["obj_func_val"], y=exp_data[exp_data["id"]==id][var], 
                            label=id, facecolors="none", edgecolors=id_colors[id], alpha=0.75)
        axes[i].set(xlabel="", ylabel="")
        axes[i].set_title(exps[i])
        axes[i].legend()
    plt.suptitle(title)
    fig.supxlabel("1-r^2")
    fig.supylabel(var)
    if save:
        plt.savefig(save_file)
    if show:
        plt.show()
    plt.close()

def plot_fit_vs_value_all(df, var, title, save_file, save, show):
    plt.figure()
    for exp in df["exp"].unique():
        plt.scatter(x=df[df["exp"]==exp]["obj_func_val"], y=df[df["exp"]==exp][var], s=20, 
                    label=exp, facecolors="none", edgecolors=group_colors[exp], alpha=0.75)
    plt.legend()
    plt.ylabel(var)
    plt.xlabel("1-r^2")
    plt.title(title)
    if save:
        plt.savefig(save_file)
    if show:
        plt.show()
    plt.close()

# plot_all_on_one(clone_growth_df, title_prefix+"\nClone Growth Rates\nObjective Functions", save_path+"clone_growth_rates_obj_func_all.png", save, show)
# plot_all_on_one(clone_intr_df, title_prefix+"\nClone Interaction\nObjective Functions", save_path+"clone_interaction_obj_func_all.png", save, show)
# plot_all_on_one(t_intr_pure_df, title_prefix+"\nT-cell Interaction Pure\nObjective Functions", save_path+"t_interaction_pure_obj_func_all.png", save, show)
# plot_all_on_one(t_intr_admix_df, title_prefix+"\nT-cell Interaction Admix\nObjective Functions", save_path+"t_interaction_obj_func_all.png", save, show)

# plot_sep_by_exp(clone_growth_df, title_prefix+"\nClone Growth Rates\nObjective Functions", save_path+"clone_growth_rates_obj_func_ind.png", save, show)
# plot_sep_by_exp(clone_intr_df, title_prefix+"\nClone Interaction\nObjective Functions", save_path+"clone_interaction_obj_func_ind.png", save, show)
# plot_sep_by_exp(t_intr_pure_df, title_prefix+"\nT-cell Interaction Pure\nObjective Functions", save_path+"t_interaction_pure_obj_func_ind.png", save, show)
# plot_sep_by_exp(t_intr_admix_df, title_prefix+"\nT-cell Interaction Admix\nObjective Functions", save_path+"t_interaction_obj_func_ind.png", save, show)



plot_fit_vs_value_all(clone_growth_df, "est_growVal", title_prefix+"\nClone Growth Rates vs Objective Functions", save_path+"obj_func/clone_growth_rates_vs_obj_func_all.png", save, show)
plot_fit_vs_value_all(clone_intr_df, "est_intrRS", title_prefix+"\nEffect of S on R vs Objective Functions", save_path+"obj_func/intrRS_vs_obj_func_all.png", save, show)
plot_fit_vs_value_all(clone_intr_df, "est_intrSR", title_prefix+"\nEffect of R on S vs Objective Functions", save_path+"obj_func/intrSR_vs_obj_func_all.png", save, show)
plot_fit_vs_value_all(t_intr_admix_df, "est_intrRT", title_prefix+"\nEffect of T on R vs Objective Functions", save_path+"obj_func/intrRT_vs_obj_func_all.png", save, show)
plot_fit_vs_value_all(t_intr_admix_df, "est_intrTR", title_prefix+"\nEffect of R on T vs Objective Functions", save_path+"obj_func/intrTR_vs_obj_func_all.png", save, show)
plot_fit_vs_value_all(t_intr_admix_df, "est_intrST", title_prefix+"\nEffect of T on S vs Objective Functions", save_path+"obj_func/intrST_vs_obj_func_all.png", save, show)
plot_fit_vs_value_all(t_intr_admix_df, "est_intrTS", title_prefix+"\nEffect of S on T vs Objective Functions", save_path+"obj_func/intrTS_vs_obj_func_all.png", save, show)

plot_fit_vs_value_by_exp(clone_growth_df, "est_growVal", title_prefix+"\nClone Growth Rates vs Objective Functions", save_path+"obj_func/clone_growth_rates_vs_obj_func_ind.png", save, show)
plot_fit_vs_value_by_exp(clone_intr_df, "est_intrRS", title_prefix+"\nEffect of S on R vs Objective Functions", save_path+"obj_func/intrRS_vs_obj_func_ind.png", save, show)
plot_fit_vs_value_by_exp(clone_intr_df, "est_intrSR", title_prefix+"\nEffect of R on S vs Objective Functions", save_path+"obj_func/intrSR_vs_obj_func_ind.png", save, show)
plot_fit_vs_value_by_exp(t_intr_admix_df, "est_intrRT", title_prefix+"\nEffect of T on R vs Objective Functions", save_path+"obj_func/intrRT_vs_obj_func_ind.png", save, show)
plot_fit_vs_value_by_exp(t_intr_admix_df, "est_intrTR", title_prefix+"\nEffect of R on T vs Objective Functions", save_path+"obj_func/intrTR_vs_obj_func_ind.png", save, show)
plot_fit_vs_value_by_exp(t_intr_admix_df, "est_intrST", title_prefix+"\nEffect of T on S vs Objective Functions", save_path+"obj_func/intrST_vs_obj_func_ind.png", save, show)
plot_fit_vs_value_by_exp(t_intr_admix_df, "est_intrTS", title_prefix+"\nEffect of S on T vs Objective Functions", save_path+"obj_func/intrTS_vs_obj_func_ind.png", save, show)
