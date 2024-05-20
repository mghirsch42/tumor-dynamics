import pandas as pd
from matplotlib import colormaps
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
from utils import get_group_colors, get_id_colors

nude_clone_intr_df = pd.read_csv("results/method5/nude_clone_interaction.csv")
b6_clone_intr_df = pd.read_csv("results/method5/b6_clone_interaction.csv")
title_prefix = "Method 5"
save_path = "figures/method5/"

save = True
show = True

nude_clone_intr_df = nude_clone_intr_df[["exp", "id", "est_intrRS", "est_intrSR", "obj_func_val"]].sort_values(["exp", "id"])
b6_clone_intr_df = b6_clone_intr_df[["exp", "id", "est_intrRS", "est_intrSR", "obj_func_val"]].sort_values(["exp", "id"])
nude_clone_intr_df_avg = nude_clone_intr_df.groupby(["exp", "id"]).mean().reset_index()
b6_clone_intr_df_avg = b6_clone_intr_df.groupby(["exp", "id"]).mean().reset_index()

group_colors = get_group_colors()
id_colors = get_id_colors()

def plot_sep_by_exp(df, var_x, var_y, title, save_file, save, show):
    exps = df["exp"].unique()
    fig, axes = plt.subplots(nrows=1, ncols=len(exps), figsize=(14,7))
    for i in range(len(exps)):
        exp_data = df[df["exp"]==exps[i]]
        for id in exp_data["id"].unique():
            axes[i].scatter(exp_data[exp_data["id"]==id][var_x], exp_data[exp_data["id"]==id][var_y], s=20, color=id_colors[id], label=id)
        # sns.scatterplot(data=exp_data, x=var_x, y=var_y, ax=axes[i], hue="id", palette=colormaps["Set1"])
        axes[i].vlines(x=0, ymin=min(min(df[var_y]),0), ymax=max(max(df[var_y]),0), color="black", linestyles="dashed")
        axes[i].hlines(y=0, xmin=min(min(df[var_x]),0), xmax=max(max(df[var_x]),0), color="black", linestyles="dashed")
        axes[i].set(xlabel="", ylabel="")
        axes[i].set_title(exps[i])
        axes[i].legend()
    plt.suptitle(title)
    fig.supxlabel(var_x)
    fig.supylabel(var_y)
    plt.tight_layout()
    if save:
        plt.savefig(save_file)
    if show:
        plt.show()
    plt.close()

def plot_all_on_one(df, var_x, var_y, title, save_file, save, show):
    plt.figure()
    for exp in df["exp"].unique():
        plt.scatter(df[df["exp"]==exp][var_x], df[df["exp"]==exp][var_y], s=20, color=group_colors[exp], label=exp, alpha=0.75)
    # sns.scatterplot(data=df, x=var_x, y=var_y, hue="exp")
    plt.vlines(x=0, ymin=min(min(df[var_y]),0), ymax=max(max(df[var_y]),0), color="black", linestyles="dashed")
    plt.hlines(y=0, xmin=min(min(df[var_x]),0), xmax=max(max(df[var_x]),0), color="black", linestyles="dashed")
    plt.title(title)
    plt.xlabel(var_x)
    plt.ylabel(var_y)
    plt.legend()
    plt.tight_layout()
    if save:
        plt.savefig(save_file)
    if show:
        plt.show()
    plt.close()

def plot_by_fit_sep_by_exp(df, var_x, var_y, title, save_file, save, show):
    exps = df["exp"].unique()
    fig, axes = plt.subplots(nrows=1, ncols=len(exps), figsize=(14,7))
    for i in range(len(exps)):
        exp_data = df[df["exp"]==exps[i]]
        sns.scatterplot(data=exp_data, x=var_x, y=var_y, ax=axes[i], hue="obj_func_val")
        axes[i].set(xlabel="", ylabel="")
        axes[i].set_title(exps[i])
        axes[i].legend()
    plt.suptitle(title)
    fig.supxlabel(var_x)
    fig.supylabel(var_y)
    plt.tight_layout()
    if save:
        plt.savefig(save_file)
    if show:
        plt.show()
    plt.close()

def plot_by_fit_all_on_one(df, var_x, var_y, title, save_file, save, show):
    plt.figure()
    sns.scatterplot(data=df, x=var_x, y=var_y, hue="obj_func_val")
    plt.title(title)
    plt.xlabel(var_x)
    plt.ylabel(var_y)
    plt.legend()
    plt.tight_layout()
    if save:
        plt.savefig(save_file)
    if show:
        plt.show()
    plt.close()

# plot_sep_by_exp(nude_clone_intr_df, "est_intrRS", "est_intrSR", title_prefix+"\nNude\nR vs S", save_path+"r_vs_s/nude_ind.png", save, show)
# plot_sep_by_exp(nude_clone_intr_df_avg, "est_intrRS", "est_intrSR", title_prefix+"\nNude\nR vs S", save_path+"r_vs_s/nude_ind_avg.png", save, show)
# plot_sep_by_exp(b6_clone_intr_df, "est_intrRS", "est_intrSR", title_prefix+"\nB6\nR vs S", save_path+"r_vs_s/b6_ind.png", save, show)
# plot_sep_by_exp(b6_clone_intr_df_avg, "est_intrRS", "est_intrSR", title_prefix+"\nB6\nR vs S", save_path+"r_vs_s/b6_ind_avg.png", save, show)

# plot_all_on_one(nude_clone_intr_df, "est_intrRS", "est_intrSR", title_prefix+"\nNude\nR vs S", save_path+"r_vs_s/nude_all.png", save, show)
# plot_all_on_one(nude_clone_intr_df_avg, "est_intrRS", "est_intrSR", title_prefix+"\nNude\nR vs S", save_path+"r_vs_s/nude_all_avg.png", save, show)
# plot_all_on_one(b6_clone_intr_df, "est_intrRS", "est_intrSR", title_prefix+"\nB6\nR vs S", save_path+"r_vs_s/b6_all.png", save, show)
# plot_all_on_one(b6_clone_intr_df_avg, "est_intrRS", "est_intrSR", title_prefix+"\nB6\nR vs S", save_path+"r_vs_s/b6_all_avg.png", save, show)

plot_by_fit_sep_by_exp(nude_clone_intr_df, "est_intrRS", "est_intrSR", title_prefix+"\nNude\nR vs S\nBy Fit", save_path+"r_vs_s/nude_ind_by_fit.png", save, show)
plot_by_fit_sep_by_exp(b6_clone_intr_df, "est_intrRS", "est_intrSR", title_prefix+"\nB6\nR vs S\nBy Fit", save_path+"r_vs_s/b6_ind_by_fit.png", save, show)
plot_by_fit_all_on_one(nude_clone_intr_df, "est_intrRS", "est_intrSR", title_prefix+"\nNude\nR vs S\nBy Fit", save_path+"r_vs_s/nude_all_by_fit.png", save, show)
plot_by_fit_all_on_one(b6_clone_intr_df, "est_intrRS", "est_intrSR", title_prefix+"\nB6\nR vs S\nBy Fit", save_path+"r_vs_s/b6_all_by_fit.png", save, show)
