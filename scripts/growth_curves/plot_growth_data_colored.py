import argparse
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

def get_id_colors():
    df = pd.read_csv("data/id_colors.csv")
    df = df.drop("Group", axis=1)
    df = df.set_index("ID")
    return df.to_dict()["Color"]

def main(data_file, save_path, show):
    
    df = pd.read_csv(data_file)
    df = df.melt(id_vars=["Group", "ID"], var_name="Day", value_name="Size").reset_index()
    df = df.dropna()
    df["Day"] = df["Day"].astype(int)
    exps = ["(100% C1)", "(80% C1; 20% C11)", "(50% C1; 50% C11)", "(20% C1; 80% C11)", "(100% C11)"]
    days = df["Day"].unique().astype(int)
    days.sort()
    id_colors = get_id_colors()
    fig, axes = plt.subplots(nrows=1, ncols=5, sharex=True, sharey=True, figsize=(15, 6))
    for i in range(len(exps)):
        exp = exps[i]
        exp_df = df[[exp in x for x in df["Group"]]]
        exp_b6 = exp_df[["A" in x for x in exp_df["Group"]]]
        exp_nude = exp_df[["nude" in x for x in exp_df["Group"]]]
        for mouse_id in exp_b6["ID"].unique():
            axes[i].plot(exp_b6[exp_b6["ID"] == mouse_id]["Day"].astype(int), exp_b6[exp_b6["ID"] == mouse_id]["Size"], 
                        color=id_colors[mouse_id], label=mouse_id)
        for mouse_id in exp_nude["ID"].unique():
            axes[i].plot(exp_nude[exp_nude["ID"] == mouse_id]["Day"].astype(int), exp_nude[exp_nude["ID"] == mouse_id]["Size"], 
                        color=id_colors[mouse_id], label=mouse_id, linestyle="dashed")
        axes[i].set_title(exp)
        axes[i].legend(loc="upper center", ncol=2, bbox_to_anchor=(0.5, -0.2))
    fig.supxlabel("Day")
    fig.supylabel("Size (mm^3)")
    fig.tight_layout()
    if save_path:
        plt.savefig(save_path+"all_colors.png")
    if show:
        plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data_file", type=str, action="store", default="data/growth_data.csv")
    parser.add_argument("-s", "--save_path", type=str, action="store", default="figures/growth_data/")
    parser.add_argument("--show", action="store_true", default=True)
    args = parser.parse_args()
    main(args.data_file, args.save_path, args.show)