import numpy as np
from matplotlib import pyplot as plt
from sklearn.metrics import r2_score
from scipy.optimize import minimize, dual_annealing
import pandas as pd
import argparse
import utils

##########
# Estimates the interaction between sublines using the mean estimated growth rates and nude mice
##########

def update_results(curr_results, exp, params, opt_results):
    curr_results["exp"].append(params["exp"])
    curr_results["id"].append(params["id"])
    curr_results["n"].append(params["n"])
    curr_results["init_totalPop"].append(params["init_totalPop"])
    curr_results["initR"].append(params["initR"])
    curr_results["initS"].append(params["initS"])
    curr_results["init_intrRS"].append(params["init_intrRS"])
    curr_results["init_intrSR"].append(params["init_intrSR"])
    curr_results["avg_growR"].append(params["avg_growR"])
    curr_results["avg_growS"].append(params["avg_growS"])
    curr_results["est_intrRS"].append(opt_results.x[0])
    curr_results["est_intrSR"].append(opt_results.x[1])
    curr_results["bounds"].append(params["bounds"])
    curr_results["obj_func_val"].append(opt_results.fun)
    return curr_results

def main(exp_file, growth_rate_file, save_file):
    params = {
        "init_intrRS": .002,
        "init_intrSR": .001,
        "bounds": ((-.1, .1), (-.1, .1))
    }
    results = {
        "exp": [],
        "id": [],
        "n": [],
        "init_totalPop": [],
        "initR": [],
        "initS": [],
        "avg_growR": [],
        "avg_growS": [],
        "init_intrRS": [],
        "init_intrSR": [],
        "bounds": [],
        "est_intrRS": [],
        "est_intrSR": [],
        "obj_func_val": [],
    }

    df = pd.read_csv(exp_file, index_col=0)
    growth_rate_df = pd.read_csv(growth_rate_file)
    params.update({"n": growth_rate_df.loc[0, "n"], "init_totalPop": growth_rate_df.loc[0, "init_totalPop"]})
    avg_growR = growth_rate_df[growth_rate_df["exp"].str.contains("B5")]["est_growVal"].mean()
    avg_growS = growth_rate_df[growth_rate_df["exp"].str.contains("B1")]["est_growVal"].mean()
    params.update({"avg_growR": avg_growR, "avg_growS": avg_growS})

    for idx, row in df.iterrows():
        if "B1" in row.name or "B5" in row.name: continue
        if not "nude" in row.name: continue
        exp = row.name
        print(exp)
        true_exp_params = {"a": row["a"], "b": row["b"], "c": row["c"]}
        params.update({"exp": exp, "id": row["id"]})
        params.update(utils.get_init_R_S(params["init_totalPop"], exp))
        
        grow_vals = {"avg_growR": params["avg_growR"], "avg_growS": params["avg_growS"]}
        init_pop_vals = {"initR": params["initR"], "initS": params["initS"]}
        opt_results = dual_annealing(utils.one_step_error_mixed,
                        x0 = [params["init_intrRS"], params["init_intrSR"]],
                        args = (params["n"], grow_vals, init_pop_vals, true_exp_params),
                        bounds = params["bounds"],
                        minimizer_kwargs={"method": "L-BFGS-B", "bounds": params["bounds"]},
                        seed = 42
                        )
        
        results = update_results(results, exp, params, opt_results)
    results_df = pd.DataFrame.from_dict(results)
    results_df = pd.merge(df, results_df, on="id")
    print(results_df)
    results_df.to_csv(save_file, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--exp_file", action="store", default="results/growth_fit_results/exp_growth.csv")
    parser.add_argument("--growth_rate_file", action="store", default="results/interaction_results/without_growT/clone_growth_rates.csv")
    parser.add_argument("--save_file", action="store", default="results/interaction_results/without_growT/clone_interaction.csv")
    args = parser.parse_args()
    main(args.exp_file, args.growth_rate_file, args.save_file)
