import numpy as np
from sklearn.metrics import r2_score
import pandas as pd

def exp_funct(data, a, b, c):
    return a * np.exp(b*data) + c

def get_init_R_S(init_totalPop, exp):
    if "B2" in exp:
        return {"initR": init_totalPop * 0.2, "initS": init_totalPop * 0.8}
    if "B3" in exp:
        return {"initR": init_totalPop * 0.5, "initS": init_totalPop * 0.5}
    if "B4" in exp:
        return {"initR": init_totalPop * 0.8, "initS": init_totalPop * 0.2}
    if "A1" in exp:
        return {"initR": 0, "initS": init_totalPop}
    if "A2" in exp:
        return {"initR": init_totalPop * 0.2, "initS": init_totalPop * 0.8}
    if "A3" in exp:
        return {"initR": init_totalPop * 0.5, "initS": init_totalPop * 0.5}
    if "A4" in exp:
        return {"initR": init_totalPop * 0.8, "initS": init_totalPop * 0.2}
    if "A5" in exp:
        return {"initR": init_totalPop, "initS": 0}
    else:
        print("experiment not found, exiting")
        exit()

def runNtimes_pure(n, initVal, growRate):
    res = [initVal]
    currVal = initVal
    for i in range(n-1):
        dv = growRate * currVal
        currVal = currVal + dv
        if currVal < 0: currVal = 0
        if currVal >= 2 ** 254: currVal = 2 ** 254
        res += [currVal]
    return np.asarray(res)

def one_step_error_pure(opt_params, n, init_totalPop, true_exp_params):
    growVal = opt_params[0]
    results = runNtimes_pure(n, init_totalPop, growVal)
    xvals = np.asarray(list(range(0, n)))
    true_vals = true_exp_params["a"] * np.exp(true_exp_params["b"] * xvals) + true_exp_params["c"]
    r2 = r2_score(results, true_vals)
    return 1 - r2


def get_group_colors():
    df = pd.read_csv("data/group_colors.csv")
    df = df.set_index("Group")
    return df.to_dict()["Color"]

def get_id_colors():
    df = pd.read_csv("data/id_colors.csv")
    df = df.drop("Group", axis=1)
    df = df.set_index("ID")
    return df.to_dict()["Color"]