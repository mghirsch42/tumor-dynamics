import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import utils

def plot_t(x, exp, run_results, save_file):
    plt.figure()
    # plt.plot(x, true_results, color="black", label="true")
    if "A1" in exp:
        plt.plot(x, run_results[:,0], color="green", label="est_S")
        plt.plot(x, run_results[:,1], color="gray", label="est_T")
    elif "A5" in exp:
        plt.plot(x, run_results[:,0], color="orange", label="est_R")
        plt.plot(x, run_results[:,1], color="gray", label="est_T")
    else:
        plt.plot(x, run_results[:,0], color="orange", label="est_R")
        plt.plot(x, run_results[:,1], color="green", label="est_S")
        plt.plot(x, run_results[:,2], color="blue", label="est_total")
        plt.plot(x, run_results[:,3], color="gray", label="est_T")
    plt.title(exp)
    plt.legend()
    plt.savefig(save_file)
    plt.show()
    plt.close()

def main(data_file, results_file, save_path):
    results_df = pd.read_csv(results_file)
    n = results_df.loc[0, "n"]
    xvals = np.linspace(start=0, stop=n, num=n)
    avg_df = results_df.groupby("exp")[["n", "initR", "initS", "initT", "growR", "growS", "est_growT",
                                       "intrRS", "intrSR", "est_intrRT", "est_intrST", "est_intrTR", "est_intrTS"]].mean().reset_index()
    print(avg_df)
    for idx, row in avg_df.iterrows():
        if "nude" in row["exp"]: continue
        print(row["exp"])
        if "A1" in row["exp"]:
            run_results = utils.runNtimes_t_pure(n, row["initS"], row["initT"], row["growS"], row["est_growT"], 
                                            row["est_intrST"], row["est_intrTS"])
        elif "A5" in row["exp"]:
            run_results = utils.runNtimes_t_pure(n, row["initR"], row["initT"], row["growR"], row["est_growT"], 
                                            row["est_intrRT"], row["est_intrTR"])
        else:
            run_results = utils.runNtimes_t(n, row["initR"], row["initS"], row["initT"], row["growR"], row["growS"], 
                        row["est_growT"], row["intrRS"], row["intrSR"], row["est_intrRT"], 
                        row["est_intrST"], row["est_intrTR"], row["est_intrTS"])
        plot_t(xvals, row["exp"], run_results, save_path+row["exp"]+".png")

if __name__ == "__main__":
    data_file = ""
    results_file = "opt_results/t_interaction.csv"
    save_path = "figures/avg_group/"
    main(data_file, results_file, save_path)