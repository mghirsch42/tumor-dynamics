import argparse
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

def exp_to_name(exp):
    if exp == "(100% C1)": return "100% Sensitive"
    elif exp == "(80% C1; 20% C11)": return "80% Sensitive; 20% Resistant"
    elif exp == "(50% C1; 50% C11)": return "50% Sensitive; 50% Resistant"
    elif exp == "(20% C1; 80% C11)": return "20% Sensitive; 80% Resistant"
    elif exp == "(100% C11)": return "100% Resistant"

def main(data_file, save_path, show):
    
    df = pd.read_csv(data_file)
    df = df.melt(id_vars=["Group", "ID"], var_name="Day", value_name="Size").reset_index()
    df = df.dropna()
    exps = ["(100% C1)", "(80% C1; 20% C11)", "(50% C1; 50% C11)", "(20% C1; 80% C11)", "(100% C11)"]
    # exps = ["(100% C1)", "(100% C11)"]
    days = df["Day"].unique().astype(int)
    days.sort()
    fig, axes = plt.subplots(nrows=1, ncols=5, sharex=True, sharey=True, figsize=(15, 4))
    # fig, axes = plt.subplots(nrows=1, ncols=2, sharex=True, sharey=True, figsize=(7, 4))
    for i in range(len(exps)):
        exp = exps[i]
        exp_df = df[df["Group"].str.contains(exp)]
        exp_b6 = exp_df[exp_df["Group"].str.contains("A")]
        exp_nude = exp_df[exp_df["Group"].str.contains("nude")]
        for mouse_id in exp_b6["ID"].unique():
            axes[i].plot(exp_b6[exp_b6["ID"] == mouse_id]["Day"].astype(int), exp_b6[exp_b6["ID"] == mouse_id]["Size"], color="tab:red")
        for mouse_id in exp_nude["ID"].unique():
            axes[i].plot(exp_nude[exp_nude["ID"] == mouse_id]["Day"].astype(int), exp_nude[exp_nude["ID"] == mouse_id]["Size"], color="mediumblue")
        nude_patch = mpatches.Patch(color="mediumblue", label="Nude")
        b6_patch = mpatches.Patch(color="tab:red", label="B6")
        # axes[i].set_title(exp[1:-1])
        axes[i].set_title(exp_to_name(exp))
        # axes[i].set_title(exp[6:-1])
    fig.supxlabel("Day")
    fig.supylabel("Size (mm^3)")
    # plt.suptitle("Growth of C1 and C11 in nude and B6 mice")
    plt.legend(handles=[nude_patch, b6_patch])
    fig.tight_layout()
    if save_path:
        plt.savefig(save_path+"all_bluered.svg")
        # plt.savefig(save_path+"c1_c11.png")
    if show:
        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data_file", type=str, action="store", default="data/growth_data_orig.csv")
    parser.add_argument("-s", "--save_path", type=str, action="store", default="figures/growth_data/")
    parser.add_argument("--show", action="store_true", default=True)
    args = parser.parse_args()
    main(args.data_file, args.save_path, args.show)