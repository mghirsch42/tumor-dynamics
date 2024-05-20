import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import argparse
from utils import exp_funct, runNtimes_pure, get_init_R_S

def rep_aggs(est_df):
    est_df = est_df[["exp", "id", "est_growVal", "obj_func_val"]]
    est_df = est_df.rename({"exp": "Group", "id": "ID"}, axis=1)
    med_df = est_df.groupby(["Group", "ID"]).median().reset_index()
    max_df = est_df.groupby(["Group", "ID"]).max().reset_index()
    min_df = est_df.groupby(["Group", "ID"]).min().reset_index()
    return med_df, max_df, min_df

def main(data_file, exp_file, est_file, save_path, save, show):
    data_df = pd.read_csv(data_file)
    exp_df = pd.read_csv(exp_file)
    est_df = pd.read_csv(est_file)

    data_df = data_df.melt(id_vars=["Group", "ID"], var_name="Time")
    data_df = data_df.dropna()
    data_df["Time"] = data_df["Time"].astype(int)
    
    exp_df = exp_df.rename({"group": "Group", "id": "ID"}, axis=1)
    med_df, max_df, min_df = rep_aggs(est_df)

    title_prefix = "Model 1"

    for idx, row in exp_df.iterrows():
        group = row["Group"]
        mouse_id = row["ID"]
        if mouse_id == 438: continue
        curr_data = data_df[data_df["ID"] == mouse_id]
        curr_est = est_df[(est_df["exp"] == group) & (est_df["id"] == mouse_id)]
        xvals = np.arange(min(curr_data["Time"]), max(curr_data["Time"])+1)
        y_true = [exp_funct(x, row["a"], row["b"], row["c"]) for x in xvals]
        medx = curr_est["est_growVal"].median()
        minx = curr_est["est_growVal"].min()
        maxx = curr_est["est_growVal"].max()
        y_med = runNtimes_pure(len(xvals), 20, medx)
        y_min = runNtimes_pure(len(xvals), 20, minx)
        y_max = runNtimes_pure(len(xvals), 20, maxx)
        print(medx)
        fig, ax = plt.subplots()
        plt.scatter(curr_data["Time"], curr_data["value"], color="black")  
        plt.plot(xvals, y_true, label="True fit", color="black") 
        plt.plot(xvals, y_med, label="Est median", color="red")
        plt.plot(xvals, y_max, label="Est min/max", color="red", linestyle="dashed")
        plt.plot(xvals, y_min, color="red", linestyle="dashed")
        label = "True Fit: C(t)={}e^({}x)+{}\nMed Est Fit: dC(t)={}C(t)dt".format(round(row["a"],2), round(row["b"],2), round(row["c"],2), round(medx, 3))
        plt.text(0.1, 2/3, label, transform=ax.transAxes)
        plt.xlabel("Time")
        plt.ylabel("Size (mm^3)")
        plt.title("{}\n{} {}".format(title_prefix, group, str(mouse_id))) 
        plt.legend(loc="upper left")
        if save:
            plt.savefig("{}/{}_{}.png".format(save_path, group, str(mouse_id)))
        if show:
            plt.show()
        plt.close()
        # exit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_file", type=str, action="store", default="data/growth_data.csv")
    parser.add_argument("--exp_file", type=str, action="store", default="results/growth_fit_results/exp_growth.csv")
    parser.add_argument("--est_file", type=str, action="store", default="results/simple_model_2/clone_growth_rates.csv")
    parser.add_argument("--save_path", type=str, action="store", default="figures/simple_model_2/eqs_curves/")
    parser.add_argument("-s", "--save", action="store_true")
    parser.add_argument("--show", action="store_true")
    args = parser.parse_args()
    main(args.data_file, args.exp_file, args.est_file, args.save_path, args.save, args.show)