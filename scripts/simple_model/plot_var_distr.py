import pandas as pd
from matplotlib import pyplot as plt
from utils import get_group_colors, get_id_colors

clone_growth_df = pd.read_csv("results/simple_model_2/clone_growth_rates.csv")
title_prefix = "Model 1"
save_path = "figures/simple_model_2_ppt/"

show = False
save = True

color_by_id = False
color_by_exp = False
single_color = False
nude_vs_b6 = True

group_colors = get_group_colors()
id_colors = get_id_colors()

min_val = clone_growth_df["est_growVal"].min()
max_val = clone_growth_df["est_growVal"].max()

# Color by id
if color_by_id:
    print(min_val, max_val)
    for exp in clone_growth_df["exp"].unique():
        curr_df = clone_growth_df[clone_growth_df["exp"] == exp]
        # print(curr_df)
        plt.figure()
        for mouse_id in curr_df["id"].unique():
            plt.hist(curr_df[curr_df["id"]==mouse_id]["est_growVal"], label=mouse_id, color=id_colors[mouse_id], alpha=0.6)
        plt.xlim(min_val, max_val)
        plt.title(title_prefix + "\n" + exp + "\nEstimated growth value")
        plt.xlabel("Growth rate")
        plt.ylabel("Count")
        plt.legend()
        plt.tight_layout()
        if save:
            plt.savefig(save_path+exp+"_by_id.png")
        if show:
            plt.show()
        plt.close()
    
# Single color
if single_color:
    for exp in clone_growth_df["exp"].unique():
        curr_df = clone_growth_df[clone_growth_df["exp"] == exp]
        plt.figure()
        plt.hist(curr_df["est_growVal"])#, color=id_colors[])
        plt.xlim(min_val, max_val)
        plt.title(title_prefix + "\n" + exp + "\nEstimated growth value")
        plt.xlabel("Growth rate")
        plt.ylabel("Count")
        plt.tight_layout()
        if save:
            plt.savefig(save_path+exp+".png")
        if show:
            plt.show()
        plt.close()

if color_by_exp:
    # B6
    curr_df = clone_growth_df[clone_growth_df["exp"].str.contains("B6")]
    plt.figure()
    for exp in curr_df["exp"].unique():
        plt.hist(curr_df[curr_df["exp"]==exp]["est_growVal"], label=exp, color=group_colors[exp], alpha=0.6)
    plt.xlim(min_val, max_val)
    plt.title(title_prefix + "\nB6\nEstimated growth value")
    plt.xlabel("Growth rate")
    plt.ylabel("Count")
    plt.legend()
    plt.tight_layout()
    if save:
        plt.savefig(save_path+"b6.png")
    if show:
        plt.show()
    plt.close()

    # Nude
    curr_df = clone_growth_df[~clone_growth_df["exp"].str.contains("B6")]
    plt.figure()
    for exp in curr_df["exp"].unique():
        plt.hist(curr_df[curr_df["exp"]==exp]["est_growVal"], label=exp, color=group_colors[exp], alpha=0.6)
    plt.xlim(min_val, max_val)
    plt.title(title_prefix + "\nNude\nEstimated growth value")
    plt.xlabel("Growth rate")
    plt.ylabel("Count")
    plt.legend()
    plt.tight_layout()
    if save:
        plt.savefig(save_path+"nude.png")
    if show:
        plt.show()
    plt.close()

if nude_vs_b6:
    plt.hist(clone_growth_df[~clone_growth_df["exp"].str.contains("B6")]["est_growVal"], label="Nude", alpha=0.6)
    plt.hist(clone_growth_df[clone_growth_df["exp"].str.contains("B6")]["est_growVal"], label="B6", alpha=0.6)
    plt.xlim(min_val, max_val)
    plt.title(title_prefix + "\nEstimated growth value")
    plt.xlabel("Growth rate")
    plt.ylabel("Count")
    plt.legend()
    plt.tight_layout()
    if save:
        plt.savefig(save_path+"nude_vs_b6.png")
    if show:
        plt.show()
    plt.close()