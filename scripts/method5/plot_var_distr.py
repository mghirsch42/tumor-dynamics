import pandas as pd
from matplotlib import pyplot as plt
from utils import get_id_colors, get_group_colors

nude_clone_growth_df = pd.read_csv("results/method5/nude_clone_growth_rates.csv")
nude_clone_intr_df = pd.read_csv("results/method5b/nude_clone_interaction.csv")
b6_clone_growth_df = pd.read_csv("results/method5/b6_clone_growth_rates.csv")
b6_clone_intr_df = pd.read_csv("results/method5b/b6_clone_interaction.csv")
title_prefix = "Method 2"
save_path = "figures/method5b_ppt/"

plot_type = "intr_by_exp" # overlap, individual, or intr_by_exp

save = True
show = True

nude_r_growth = nude_clone_growth_df[nude_clone_growth_df["exp"] == "Grp. B5 nude (100% C11)"].sort_values(["exp", "id"])
nude_s_growth = nude_clone_growth_df[nude_clone_growth_df["exp"] == "Grp. B1 nude (100% C1)"].sort_values(["exp", "id"])
b6_r_growth = b6_clone_growth_df[b6_clone_growth_df["exp"] == "Grp. A5 B6 (100% C11)"].sort_values(["exp", "id"])
b6_s_growth = b6_clone_growth_df[b6_clone_growth_df["exp"] == "Grp. A1 B6 (100% C1)"].sort_values(["exp", "id"])

group_colors = get_group_colors()
id_colors = get_id_colors()


max_grow_val = max(nude_clone_growth_df["est_growVal"].max(), b6_clone_growth_df["est_growVal"].max())
min_grow_val = min(nude_clone_growth_df["est_growVal"].min(), b6_clone_growth_df["est_growVal"].min())

max_intr_val = max(nude_clone_intr_df["est_intrRS"].max(), nude_clone_intr_df["est_intrSR"].max(),
                    b6_clone_intr_df["est_intrRS"].max(), b6_clone_intr_df["est_intrSR"].max())
min_intr_val = min(nude_clone_intr_df["est_intrRS"].min(), nude_clone_intr_df["est_intrSR"].min(),
                    b6_clone_intr_df["est_intrRS"].min(), b6_clone_intr_df["est_intrSR"].min())



if plot_type == "individual": 
    # Nude R
    plt.figure()
    for id in nude_r_growth["id"].unique():
        print(nude_r_growth[nude_r_growth["id"] == id]["est_growVal"])
        plt.hist(nude_r_growth[nude_r_growth["id"] == id]["est_growVal"], label=id, alpha=0.75, color=id_colors[id])
    plt.title(title_prefix + "\nNude\nR growth rate")
    plt.xlim(min_grow_val, max_grow_val)
    plt.legend()
    plt.tight_layout()
    if save:
        plt.savefig(save_path+"nude_growR.png")
    if show:
        plt.show()
    plt.close()
    # Nude S
    plt.figure()
    for id in nude_s_growth["id"].unique():
        plt.hist(nude_s_growth[nude_s_growth["id"] == id]["est_growVal"], label=id, alpha=0.75, color=id_colors[id])
    plt.title(title_prefix + "\nNude\nS growth rate")
    plt.xlim(min_grow_val, max_grow_val)
    plt.legend()
    plt.tight_layout()
    if save:
        plt.savefig(save_path+"nude_growS.png")
    if show:
        plt.show()
    plt.close()
    # Nude intrRS
    plt.figure()
    plt.hist(nude_clone_intr_df["est_intrRS"])
    plt.xlim(min_intr_val, max_intr_val)
    plt.title(title_prefix + "\nNude\nInfluence of S on R")
    plt.tight_layout()
    if save:
        plt.savefig(save_path+"r_vs_s/nude_intrRS.png")
    if show:
        plt.show()
    plt.close()
    # Nude intrSR
    plt.figure()
    plt.hist(nude_clone_intr_df["est_intrSR"])
    plt.title(title_prefix + "\nNude\nInfluence of R on S")
    plt.xlim(min_intr_val, max_intr_val)
    plt.tight_layout()
    if save:
        plt.savefig(save_path+"r_vs_s/nude_intrSR.png")
    if show:
        plt.show()
    plt.close()
    # B6 R
    plt.figure()
    for id in b6_r_growth["id"].unique():
        plt.hist(b6_r_growth[b6_r_growth["id"] == id]["est_growVal"], label=id, alpha=0.75, color=id_colors[id])
    plt.title(title_prefix + "\nB6\nR growth rate")
    plt.xlim(min_grow_val, max_grow_val)
    plt.legend()
    plt.tight_layout()
    if save:
        plt.savefig(save_path+"b6_growR.png")
    if show:
        plt.show()
    plt.close()
    # B6 S
    plt.figure()
    for id in b6_s_growth["id"].unique():
        plt.hist(b6_s_growth[b6_s_growth["id"] == id]["est_growVal"], label=id, alpha=0.75, color=id_colors[id])
    plt.title(title_prefix + "\nB6\nS growth rate")
    plt.xlim(min_grow_val, max_grow_val)
    plt.legend()
    plt.tight_layout()
    if save:
        plt.savefig(save_path+"b6_growS.png")
    if show:
        plt.show()
    plt.close()
    # B6 intrRS
    plt.figure()
    plt.hist(b6_clone_intr_df["est_intrRS"])
    plt.title(title_prefix + "\nB6\nInfluence of S on R")
    plt.xlim(min_intr_val, max_intr_val)
    plt.tight_layout()
    if save:
        plt.savefig(save_path+"r_vs_s/b6_intrRS.png")
    if show:
        plt.show()
    plt.close()
    # B6 intrSR
    plt.figure()
    plt.hist(b6_clone_intr_df["est_intrSR"])
    plt.title(title_prefix + "\nB6\nInfluence of R on S")
    plt.xlim(min_intr_val, max_intr_val)
    plt.tight_layout()
    if save:
        plt.savefig(save_path+"r_vs_s/b6_intrSR.png")
    if show:
        plt.show()
    plt.close()

if plot_type == "overlap":
    # R
    plt.figure()
    plt.hist(nude_r_growth["est_growVal"], label="Nude", alpha=0.75)
    plt.hist(b6_r_growth["est_growVal"], label="B6", alpha=0.75)
    plt.title(title_prefix + "\nR\nGrowth rate")
    plt.xlim(min_grow_val, max_grow_val)
    plt.legend()
    plt.tight_layout()
    if save:
        plt.savefig(save_path+"overlap_growR.png")
    if show:
        plt.show()
    plt.close()
    # S
    plt.figure()
    plt.hist(nude_s_growth["est_growVal"], label="Nude", alpha=0.75)
    plt.hist(b6_s_growth["est_growVal"], label="B6", alpha=0.75)
    plt.title(title_prefix + "\nS\nGrowth rate")
    plt.xlim(min_grow_val, max_grow_val)
    plt.legend()
    plt.tight_layout()
    if save:
        plt.savefig(save_path+"overlap_growS.png")
    if show:
        plt.show()
    plt.close()
    # intrRS
    plt.figure()
    plt.hist(nude_clone_intr_df["est_intrRS"], label="Nude", alpha=0.75)
    plt.hist(b6_clone_intr_df["est_intrRS"], label="B6", alpha=0.75)
    plt.title(title_prefix + "\nInfluence of S on R")
    plt.xlim(min_intr_val, max_intr_val)
    plt.legend()
    plt.tight_layout()
    if save:
        plt.savefig(save_path+"r_vs_s/overlap_intrRS.png")
    if show:
        plt.show()
    plt.close()
    # intrSR
    plt.figure()
    plt.hist(nude_clone_intr_df["est_intrSR"], label="Nude", alpha=0.75)
    plt.hist(b6_clone_intr_df["est_intrSR"], label="B6", alpha=0.75)
    plt.title(title_prefix + "\nInfluence of R on S")
    plt.xlim(min_intr_val, max_intr_val)
    plt.legend()
    plt.tight_layout()
    if save:
        plt.savefig(save_path+"r_vs_s/overlap_intrSR.png")
    if show:
        plt.show()
    plt.close()

if plot_type == "intr_by_exp":
    plt.figure()
    for exp in b6_clone_intr_df["exp"].unique():
        plt.hist(b6_clone_intr_df[b6_clone_intr_df["exp"] == exp]["est_intrRS"], label=exp, alpha=0.75, color=group_colors[exp])
    plt.title(title_prefix + "\nB6\nInfluence of S on R")
    plt.xlim(min_intr_val, max_intr_val)
    plt.legend()
    plt.tight_layout()
    if save:
        plt.savefig(save_path+"r_vs_s/b6_intrRS_by_exp.png")
    if show:
        plt.show()
    plt.close()

    plt.figure()
    for exp in b6_clone_intr_df["exp"].unique():
        plt.hist(b6_clone_intr_df[b6_clone_intr_df["exp"] == exp]["est_intrSR"], label=exp, alpha=0.75, color=group_colors[exp])
    plt.title(title_prefix + "\nB6\nInfluence of R on S")
    plt.xlim(min_intr_val, max_intr_val)
    plt.legend()
    plt.tight_layout()
    if save:
        plt.savefig(save_path+"r_vs_s/b6_intrSR_by_exp.png")
    if show:
        plt.show()
    plt.close()

    
    plt.figure()
    for exp in nude_clone_intr_df["exp"].unique():
        plt.hist(nude_clone_intr_df[nude_clone_intr_df["exp"] == exp]["est_intrRS"], label=exp, alpha=0.75, color=group_colors[exp])
    plt.title(title_prefix + "\nNude\nInfluence of S on R")
    plt.xlim(min_intr_val, max_intr_val)
    plt.legend()
    plt.tight_layout()
    if save:
        plt.savefig(save_path+"r_vs_s/nude_intrRS_by_exp.png")
    if show:
        plt.show()
    plt.close()

    plt.figure()
    for exp in nude_clone_intr_df["exp"].unique():
        plt.hist(nude_clone_intr_df[nude_clone_intr_df["exp"] == exp]["est_intrSR"], label=exp, alpha=0.75, color=group_colors[exp])
    plt.title(title_prefix + "\nNude\nInfluence of R on S")
    plt.xlim(min_intr_val, max_intr_val)
    plt.legend()
    plt.tight_layout()
    if save:
        plt.savefig(save_path+"r_vs_s/nude_intrSR_by_exp.png")
    if show:
        plt.show()
    plt.close()