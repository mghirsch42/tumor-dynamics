import pandas as pd
from matplotlib import colormaps
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
from utils import get_group_colors, get_id_colors

df = pd.read_csv("results/method4a/t_interaction.csv")
rs_df = pd.read_csv("results/method4a/clone_interaction.csv")
save_path = "figures/method4a/"
title_prefix = "Method 4a"

show = True
save = True

rt_df = df[["exp", "id", "est_intrRT", "est_intrTV", "obj_func_val"]]
st_df = df[["exp", "id", "est_intrST", "est_intrTV", "obj_func_val"]]

rt_df = rt_df.dropna().sort_values(["exp", "id"])
st_df = st_df.dropna().sort_values(["exp", "id"])
rs_df = rs_df.dropna().sort_values(["exp", "id"])
rt_df_avg = rt_df.groupby(["exp", "id"]).mean().reset_index()
st_df_avg = st_df.groupby(["exp", "id"]).mean().reset_index()
rs_df_avg = rs_df.groupby(["exp", "id"])[["est_intrRS", "est_intrSR"]].mean().reset_index()

group_colors = get_group_colors()
id_colors = get_id_colors()

def plot_sep_by_exp(df, var_x, var_y, title, save_file, save, show):
    exps = df["exp"].unique()
    fig, axes = plt.subplots(nrows=1, ncols=len(exps), figsize=(14,7))
    for i in range(len(exps)):
        exp_data = df[df["exp"]==exps[i]]
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

# plot_sep_by_exp(rt_df, "est_intrRT", "est_intrTV", title_prefix+"\nR vs T", save_path+"r_vs_t/ind.png", save, show)
# plot_sep_by_exp(rt_df_avg, "est_intrRT", "est_intrTV", title_prefix+"\nR vs T", save_path+"r_vs_t/ind_avg.png", save, show)
# plot_sep_by_exp(st_df, "est_intrST", "est_intrTV", title_prefix+"\nS vs T", save_path+"s_vs_t/ind.png", save, show)
# plot_sep_by_exp(st_df_avg, "est_intrST", "est_intrTV", title_prefix+"\nS vs T", save_path+"s_vs_t/ind_avg.png", save, show)
# plot_sep_by_exp(rs_df, "est_intrRS", "est_intrSR", title_prefix+"\nR vs S", save_path+"r_vs_s/ind.png", save, show)
# plot_sep_by_exp(rs_df_avg, "est_intrRS", "est_intrSR", title_prefix+"\nR vs S", save_path+"r_vs_s/ind_avg.png", save, show)

# plot_all_on_one(rt_df, "est_intrRT", "est_intrTV", title_prefix+"\nR vs T", save_path+"r_vs_t/all.png", save, show)
# plot_all_on_one(rt_df_avg, "est_intrRT", "est_intrTV", title_prefix+"\nR vs T", save_path+"r_vs_t/all_avg.png", save, show)
# plot_all_on_one(st_df, "est_intrST", "est_intrTV", title_prefix+"\nS vs T", save_path+"s_vs_t/all.png", save, show)
# plot_all_on_one(st_df_avg, "est_intrST", "est_intrTV", title_prefix+"\nS vs T", save_path+"s_vs_t/all_avg.png", save, show)
# plot_all_on_one(rs_df, "est_intrRS", "est_intrSR", title_prefix+"\nR vs S", save_path+"r_vs_s/all.png", save, show)
# plot_all_on_one(rs_df_avg, "est_intrRS", "est_intrSR", title_prefix+"\nR vs S", save_path+"r_vs_s/all_avg.png", save, show)

plot_by_fit_sep_by_exp(rt_df, "est_intrRT", "est_intrTV", title_prefix+"\nR vs T\nBy Fit", save_path+"r_vs_t/ind_by_fit.png", save, show)
plot_by_fit_sep_by_exp(st_df, "est_intrST", "est_intrTV", title_prefix+"\nS vs T\nBy Fit", save_path+"s_vs_t/ind_by_fit.png", save, show)
plot_by_fit_sep_by_exp(rs_df, "est_intrRS", "est_intrSR", title_prefix+"\nR vs S\nBy Fit", save_path+"r_vs_s/ind_by_fit.png", save, show)

plot_by_fit_all_on_one(rt_df, "est_intrRT", "est_intrTV", title_prefix+"\nR vs T\nBy Fit", save_path+"r_vs_t/all_by_fit.png", save, show)
plot_by_fit_all_on_one(st_df, "est_intrST", "est_intrTV", title_prefix+"\nS vs T\nBy Fit", save_path+"s_vs_t/all_by_fit.png", save, show)
plot_by_fit_all_on_one(rs_df, "est_intrRS", "est_intrSR", title_prefix+"\nR vs S\nBy Fit", save_path+"r_vs_s/all_by_fit.png", save, show)
