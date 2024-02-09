import numpy as np
from sklearn.metrics import r2_score

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

def runNtimes_mixed(n, initR, initS, growR, growS, intrRS, intrSR):
    res = [[initR, initS, initR+initS]]
    currS = initS
    currR = initR
    for i in range(n-1):
        dr = growR * currR + intrRS * currR * currS
        ds = growS * currS + intrSR * currS * currR
        currR = currR + dr
        currS = currS + ds
        if currR < 0: currR = 0
        if currS < 0: currS = 0
        if currR >= 2 ** 254: currR = 2 ** 254
        if currS >= 2 ** 254: currS = 2 ** 254
        res += [[currR, currS, currR+currS]]
    return np.asarray(res)

def one_step_error_mixed(params, n, grow_vals, init_pop_vals, true_exp_params):
    intrRS = params[0]; intrSR = params[1]
    results = runNtimes_mixed(n, init_pop_vals["initR"], init_pop_vals["initS"], 
                              grow_vals["avg_growR"], grow_vals["avg_growR"], intrRS, intrSR)
    xvals = np.asarray(list(range(0, n)))
    true_vals = true_exp_params["a"] * np.exp(true_exp_params["b"] * xvals) + true_exp_params["c"]
    r2 = r2_score(results[:, 2], true_vals)
    return 1 - r2

def runNtimes_t_pure(n, initVal, initT, growVal, growT, intrVT, intrTV):
    res = [[initVal, initT]]
    currVal = initVal
    currT = initT
    for i in range(n-1):
        dv = growVal * currVal + intrVT * currVal * currT
        dt = growT * currT + intrTV * currVal * currT
        currVal = currVal + dv
        currT = currT + dt
        if currVal < 0: currVal = 0
        if currT < 0: currT = 0
        if currVal >= 2 ** 254: currVal = 2 ** 254
        if currT >= 2 ** 254: currT = 2 ** 254
        res += [[currVal, currT]]
    return np.asarray(res)

def one_step_error_t_pure(params, n, initVal, initT, growVal, true_exp_params):
    growT = params[0]; intrVT = params[1]; intrTV = params[2]
    results = runNtimes_t_pure(n, initVal, initT, growVal, growT, intrVT, intrTV)
    xvals = np.asarray(list(range(0, n)))
    true_vals = true_exp_params["a"] * np.exp(true_exp_params["b"] * xvals) + true_exp_params["c"]
    r2 = r2_score(results[:, 0], true_vals)
    return 1 - r2

def runNtimes_t(n, initR, initS, initT, growR, growS, growT, intrRS, intrSR, intrRT, intrST, intrTR, intrTS):
    res = [[initR, initS, initR+initS, initT]]
    currS = initS
    currR = initR
    currT = initT
    for i in range(n-1):
        dr = growR * currR + intrRS * currR * currS + intrRT * currR * currT
        ds = growS * currS + intrSR * currS * currR + intrST * currS * currT
        dt = growT * currT + intrTR * currT * currR + intrTS * currR * currS
        currR = currR + dr
        currS = currS + ds
        currT = currT + dt
        if currR < 0: currR = 0
        if currS < 0: currS = 0
        if currT < 0: currT = 0
        if currR >= 2 ** 254: currR = 2 ** 254
        if currS >= 2 ** 254: currS = 2 ** 254
        if currT >= 2 ** 254: currT = 2 ** 254
        res += [[currR, currS, currR+currS, currT]]
    return np.asarray(res)

def one_step_error_t(params, n, grow_vals, init_pop_vals, intr_vals, true_exp_params):
    growT = params[0]; intrRT = params[1]; intrST = params[2]; intrTR = params[3]; intrTS = params[4]
    results = runNtimes_t(n, init_pop_vals["initR"], init_pop_vals["initS"], init_pop_vals["initT"],
                              grow_vals["avg_growR"], grow_vals["avg_growR"], growT, intr_vals["avg_intrRS"], intr_vals["avg_intrSR"],
                              intrRT, intrST, intrTR, intrTS)
    xvals = np.asarray(list(range(0, n)))
    true_vals = true_exp_params["a"] * np.exp(true_exp_params["b"] * xvals) + true_exp_params["c"]
    r2 = r2_score(results[:, 2], true_vals)
    return 1 - r2