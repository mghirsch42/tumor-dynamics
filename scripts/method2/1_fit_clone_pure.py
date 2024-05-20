import numpy as np
from matplotlib import pyplot as plt
from sklearn.metrics import r2_score
from scipy.optimize import minimize, dual_annealing
import pandas as pd
import argparse
import utils

##########
# Calculates the base growth rate of the subline using the experiments with 
# only one subline in the nude mice
##########

def update_results(curr_results, exp, params, opt_results):
    curr_results["exp"].append(params["exp"])
    curr_results["id"].append(params["id"])
    curr_results["n"].append(params["n"])
    curr_results["init_totalPop"].append(params["init_totalPop"])
    curr_results["init_growVal"].append(params["init_growVal"])
    curr_results["est_growVal"].append(opt_results.x[0])
    curr_results["bounds"].append(params["bounds"])
    curr_results["obj_func_val"].append(opt_results.fun)
    return curr_results

def main(exp_file, save_file):
    params = {
        "n": 50,
        "init_totalPop": 20,
        "init_growVal": .002,
        "bounds": [(0, 0.5)]
    }
    results = {
        "exp": [],
        "id": [],
        "n": [],
        "init_totalPop": [],
        "init_growVal": [],
        "bounds": [],
        "est_growVal": [],
        "obj_func_val": [],
    }

    df = pd.read_csv(exp_file, index_col=0)

    for idx, row in df.iterrows():
        if not ("B1" in row.name or "B5" in row.name): continue
        exp = row.name
        print(exp)
        true_exp_params = {"a": row["a"], "b": row["b"], "c": row["c"]}
        params.update({"exp": exp, "id": row["id"]})

        opt_results = dual_annealing(utils.one_step_error_pure,
                            x0 = [params["init_growVal"]],
                            args = (params["n"], params["init_totalPop"], true_exp_params),
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
    parser.add_argument("--save_file", action="store", default="results/interaction_results/without_growT/clone_growth_rates.csv")
    args = parser.parse_args()
    main(args.exp_file, args.save_file)