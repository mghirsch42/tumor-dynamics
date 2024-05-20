import pandas as pd
from matplotlib import pyplot as plt
from utils import get_group_colors, get_id_colors

nude_clone_growth_df = pd.read_csv("results/method5/nude_clone_growth_rates.csv")
nude_clone_intr_df = pd.read_csv("results/method5/nude_clone_interaction.csv")
b6_clone_growth_df = pd.read_csv("results/method5/b6_clone_growth_rates.csv")
b6_clone_intr_df = pd.read_csv("results/method5/b6_clone_interaction.csv")
title_prefix = "Method 5"
save_path = "figures/method5/"

save = False
show = True

nude_clone_growth_df = nude_clone_growth_df[["exp", "id", "est_growVal", "obj_func_val"]].sort_values(["exp", "id"])
nude_clone_intr_df = nude_clone_intr_df[["exp", "id", "est_intrRS", "est_intrSR", "obj_func_val"]].sort_values(["exp", "id"])
b6_clone_growth_df = b6_clone_growth_df[["exp", "id", "est_growVal", "obj_func_val"]].sort_values(["exp", "id"])
b6_clone_intr_df = b6_clone_intr_df[["exp", "id", "est_intrRS", "est_intrSR", "obj_func_val"]].sort_values(["exp", "id"])

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

plot_all_on_one(nude_clone_intr_df, title_prefix+"\nNude Objective Functions", save_path+"nude_obj_func_all.png", save, show)
plot_all_on_one(b6_clone_intr_df, title_prefix+"\nB6 Objective Functions", save_path+"b6_obj_func_all.png", save, show)
plot_sep_by_exp(nude_clone_intr_df, title_prefix+"\nNude Objective Functions", save_path+"nude_obj_func_ind.png", save, show)
plot_sep_by_exp(b6_clone_intr_df, title_prefix+"\nB6 Objective Functions", save_path+"b6_obj_func_ind.png", save, show)


plot_fit_vs_value_all(nude_clone_growth_df, "est_growVal", title_prefix+"\nNude Clone Growth Rates vs Objective Functions", save_path+"obj_func/nude_clone_growth_rates_vs_obj_func_all.png", save, show)
plot_fit_vs_value_all(nude_clone_intr_df, "est_intrRS", title_prefix+"\nNude Effect of S on R vs Objective Functions", save_path+"obj_func/nude_intrRS_vs_obj_func_all.png", save, show)
plot_fit_vs_value_all(nude_clone_intr_df, "est_intrSR", title_prefix+"\nNude Effect of R on S vs Objective Functions", save_path+"obj_func/nude_intrSR_vs_obj_func_all.png", save, show)
plot_fit_vs_value_all(b6_clone_growth_df, "est_growVal", title_prefix+"\nB6 Clone Growth Rates vs Objective Functions", save_path+"obj_func/b6_clone_growth_rates_vs_obj_func_all.png", save, show)
plot_fit_vs_value_all(b6_clone_intr_df, "est_intrRS", title_prefix+"\nB6 Effect of S on R vs Objective Functions", save_path+"obj_func/b6_intrRS_vs_obj_func_all.png", save, show)
plot_fit_vs_value_all(b6_clone_intr_df, "est_intrSR", title_prefix+"\nB6 Effect of R on S vs Objective Functions", save_path+"obj_func/b6_intrSR_vs_obj_func_all.png", save, show)

plot_fit_vs_value_by_exp(nude_clone_growth_df, "est_growVal", title_prefix+"\nNude Clone Growth Rates vs Objective Functions", save_path+"obj_func/nude_clone_growth_rates_vs_obj_func_ind_10.png", save, show)
plot_fit_vs_value_by_exp(nude_clone_intr_df, "est_intrRS", title_prefix+"\nNude Effect of S on R vs Objective Functions", save_path+"obj_func/nude_intrRS_vs_obj_func_ind_10.png", save, show)
plot_fit_vs_value_by_exp(nude_clone_intr_df, "est_intrSR", title_prefix+"\nNude Effect of R on S vs Objective Functions", save_path+"obj_func/nude_intrSR_vs_obj_func_ind_10.png", save, show)
plot_fit_vs_value_by_exp(b6_clone_growth_df, "est_growVal", title_prefix+"\nB6 Clone Growth Rates vs Objective Functions", save_path+"obj_func/b6_clone_growth_rates_vs_obj_func_ind_10.png", save, show)
plot_fit_vs_value_by_exp(b6_clone_intr_df, "est_intrRS", title_prefix+"\nB6 Effect of S on R vs Objective Functions", save_path+"obj_func/b6_intrRS_vs_obj_func_ind_10.png", save, show)
plot_fit_vs_value_by_exp(b6_clone_intr_df, "est_intrSR", title_prefix+"\nB6 Effect of R on S vs Objective Functions", save_path+"obj_func/b6_intrSR_vs_obj_func_ind_10.png", save, show)
