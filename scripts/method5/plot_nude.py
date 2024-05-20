import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import utils

def plot_nude(x, exp, run_results, true_results, save_file):
    plt.figure()
    plt.plot(x, true_results, color="black", label="true")
    if "B1" in exp:
        plt.plot(x, run_results, color="limegreen", label="est_S")
    elif "B5" in exp:
        plt.plot(x, run_results, color="orange", label="est_R")
    else:
        plt.plot(x, run_results[:,0], color="orange", label="est_R")
        plt.plot(x, run_results[:,1], color="limegreen", label="est_S")
        plt.plot(x, run_results[:,2], color="blue", label="est_total")
    plt.title(exp)
    plt.legend()
    # plt.savefig(save_file)
    plt.show()
    plt.close()

def main(pure_file, inter_file, save_path):
    n = 50
    pure_df = pd.read_csv(pure_file)
    inter_df = pd.read_csv(inter_file)
    xvals = np.linspace(start=0, stop=n, num=n)
    for idx, row in pure_df.iterrows():
        print(row["exp"])
        true_results = utils.exp_funct(xvals, row["a"], row["b"], row["c"])
        run_results = utils.runNtimes_pure(n, row["init_totalPop"], row["est_growVal"])
        plot_nude(xvals, row["exp"]+" "+str(row["id"]), run_results, true_results, save_path+row["exp"]+" "+str(row["id"])+".png")
    for idx, row in inter_df.iterrows():
        print(row["exp"])
        true_results = utils.exp_funct(xvals, row["a"], row["b"], row["c"])
        run_results = utils.runNtimes_mixed(n, row["initR"], row["initS"], row["avg_growR"], row["avg_growS"],
                                            row["est_intrRS"], row["est_intrSR"])
        plot_nude(xvals, row["exp"]+" "+str(row["id"]), run_results, true_results, save_path+row["exp"]+str(row["id"])+".png")
        
if __name__ == "__main__":
    pure_file = "results/interaction_results/without_growT/clone_growth_rates.csv"
    inter_file = "results/interaction_results/without_growT/clone_interaction.csv"
    save_path = "figures/interaction_figures/without_growT/"
    main(pure_file, inter_file, save_path)