from matplotlib import pyplot as plt
import numpy as np
import utils

def plot_t(x, ratio, run_results, save_file):
    plt.figure()
    # plt.plot(x, true_results, color="black", label="true")
    if ratio == 1:
        plt.plot(x, run_results[:,0], color="green", label="est_S")
        plt.plot(x, run_results[:,1], color="gray", label="est_T")
    elif ratio == 0:
        plt.plot(x, run_results[:,0], color="orange", label="est_R")
        plt.plot(x, run_results[:,1], color="gray", label="est_T")
    else:
        plt.plot(x, run_results[:,0], color="orange", label="est_R")
        plt.plot(x, run_results[:,1], color="green", label="est_S")
        plt.plot(x, run_results[:,2], color="blue", label="est_total")
        plt.plot(x, run_results[:,3], color="gray", label="est_T")
    plt.title(ratio_to_name(ratio))
    plt.legend()
    plt.savefig(save_file)
    plt.show()
    plt.close()

def ratio_to_name(ratio):
    if ratio == 1: return "100% C1"
    if ratio == 0.8: return "80% C1; 20% C11"
    if ratio == 0.5: return "50% C1; 50% C11"
    if ratio == 0.2: return "20% C1; 80% C11"
    if ratio == 0: return "100% C11"

n = 50
init_totalPop = 20
growR = 0.122600108704449
growS = 0.163956613823342
intrRS = -0.0166116392966594
intrSR = 0.0165707388286061
growT = 0.215030702
intrRT = -0.009021058
intrST = -0.058542665
intrTR = -0.038549046
intrTS = 0.033342264

for ratio in [1, 0.8, 0.5, 0.2, 0]:
    initR = init_totalPop * (1-ratio)
    initS = init_totalPop * ratio
    if ratio == 1: initT = 0.6
    if ratio == 0.8 or ratio == 0.5: initT = 0.4
    if ratio == 0.2 or 0: initT = 0.2

    if ratio == 1:
        run_results = utils.runNtimes_t_pure(n, initS, initT, growS, growT, intrST, intrTS)
    elif ratio == 0:
        run_results = utils.runNtimes_t_pure(n, initR, initT, growR, growT, intrRT, intrTR)
    else:
        run_results = utils.runNtimes_t(n, initR, initS, initT, growR, growS, growT, intrRS, intrSR, intrRT, intrST, intrTR, intrTS)

    xvals = np.linspace(start=0, stop=n, num=n)
    plot_t(xvals, ratio, run_results, "figures/avg_all/{}.png".format(ratio_to_name(ratio)))
