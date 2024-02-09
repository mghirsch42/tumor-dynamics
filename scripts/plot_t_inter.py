import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import utils

def plot_t(x, exp, run_results, true_results, save_file):
    plt.figure()
    plt.plot(x, true_results, color="black", label="true")
    if "A1" in exp:
        plt.plot(x, run_results[:,0], color="limegreen", label="est_S")
        plt.plot(x, run_results[:,1], color="gray", label="est_T")
    elif "A5" in exp:
        plt.plot(x, run_results[:,0], color="orange", label="est_R")
        plt.plot(x, run_results[:,1], color="gray", label="est_T")
    else:
        plt.plot(x, run_results[:,0], color="orange", label="est_R")
        plt.plot(x, run_results[:,1], color="limegreen", label="est_S")
        plt.plot(x, run_results[:,2], color="blue", label="est_total")
        plt.plot(x, run_results[:,3], color="gray", label="est_T")
    plt.title(exp)
    plt.legend()
    # plt.savefig(save_file)
    plt.show()
    plt.close()

def main(data_file, results_file, save_path):
    n = 50
    results_df = pd.read_csv(results_file)
    xvals = np.linspace(start=0, stop=n, num=n)
    for idx, row in results_df.iterrows():
        if "nude" in row["exp"]: continue
        print(row["exp"])
        true_results = utils.exp_funct(xvals, row["a"], row["b"], row["c"])
        if "A1" in row["exp"]:
            run_results = utils.runNtimes_t_pure(n, row["initS"], row["initT"], row["avg_growS"], row["est_growT"], 
                                            row["est_intrST"], row["est_intrTS"])
        elif "A5" in row["exp"]:
            run_results = utils.runNtimes_t_pure(n, row["initR"], row["initT"], row["avg_growR"], row["est_growT"], 
                                            row["est_intrRT"], row["est_intrTR"])
        else:
            run_results = utils.runNtimes_t(n, row["initR"], row["initS"], row["initT"], row["avg_growR"], row["avg_growS"], 
                        row["est_growT"], row["avg_intrRS"], row["avg_intrSR"], row["est_intrRT"], 
                        row["est_intrST"], row["est_intrTR"], row["est_intrTS"])
        plot_t(xvals, row["exp"]+str(row["id"]), run_results, true_results, save_path+row["exp"]+str(row["id"])+".png")

if __name__ == "__main__":
    data_file = ""
    results_file = "results/interaction_results/t_interaction.csv"
    save_path = "figures/interaction_figures/"
    main(data_file, results_file, save_path)