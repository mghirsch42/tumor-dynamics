import argparse
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

def main(data_file, save_path, show):
    
    df = pd.read_csv(data_file)
    df = df.melt(id_vars=["Group", "ID"], var_name="Day", value_name="Size").reset_index()
    df = df.dropna()
    exps = ["(100% C1)", "(80% C1; 20% C11)", "(50% C1; 50% C11)", "(20% C1; 80% C11)", "(100% C11)"]
    days = df["Day"].unique().astype(int)
    days.sort()
    fig, axes = plt.subplots(nrows=1, ncols=5, sharex=True, sharey=True, figsize=(15, 4))
    for i in range(len(exps)):
        exp = exps[i]
        exp_df = df[df["Group"].str.contains(exp)]
        exp_b6 = exp_df[exp_df["Group"].str.contains("A")]
        exp_nude = exp_df[exp_df["Group"].str.contains("nude")]
        for mouse_id in exp_b6["ID"].unique():
            axes[i].plot(exp_b6[exp_b6["ID"] == mouse_id]["Day"].astype(int), exp_b6[exp_b6["ID"] == mouse_id]["Size"], color="C1")
        for mouse_id in exp_nude["ID"].unique():
            axes[i].plot(exp_nude[exp_nude["ID"] == mouse_id]["Day"].astype(int), exp_nude[exp_nude["ID"] == mouse_id]["Size"], color="C0")
        nude_patch = mpatches.Patch(color="C0", label="Nude")
        b6_patch = mpatches.Patch(color="C1", label="B6")
        axes[i].set_title(exp)
    fig.supxlabel("Day")
    fig.supylabel("Size (mm^3)")
    plt.legend(handles=[nude_patch, b6_patch])
    fig.tight_layout()
    # if save_path:
    #     plt.savefig(save_path+"all.png")
    if show:
        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data_file", type=str, action="store", default="data/growth_data.csv")
    parser.add_argument("-s", "--save_path", type=str, action="store", default="figures/growth_data/")
    parser.add_argument("--show", action="store_true", default=True)
    args = parser.parse_args()
    main(args.data_file, args.save_path, args.show)