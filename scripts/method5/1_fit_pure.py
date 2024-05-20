import numpy as np
from scipy.optimize import dual_annealing
import pandas as pd
import argparse
import utils

##########
# Calculates the base growth rate of the subline using the experiments with 
# only one subline in the nude mice
##########

def update_results(curr_results, params, opt_results):
    curr_results["exp"].append(params["exp"])
    curr_results["id"].append(params["id"])
    curr_results["n"].append(params["n"])
    curr_results["init_totalPop"].append(params["init_totalPop"])
    curr_results["init_growVal"].append(params["init_growVal"])
    curr_results["est_growVal"].append(opt_results.x[0])
    curr_results["bounds"].append(params["bounds"])
    curr_results["obj_func_val"].append(opt_results.fun)
    return curr_results

def one_run(exp_file, params):
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
        if not ("B1" in row.name or "B5" in row.name or "A1" in row.name or "A5" in row.name): continue
        exp = row.name
        print(exp)
        true_exp_params = {"a": row["a"], "b": row["b"], "c": row["c"]}
        params.update({"exp": exp, "id": row["id"]})

        opt_results = dual_annealing(utils.one_step_error_pure,
                            x0 = [params["init_growVal"]],
                            args = (params["n"], params["init_totalPop"], true_exp_params),
                            bounds = params["bounds"],
                            minimizer_kwargs={"method": "L-BFGS-B", "bounds": params["bounds"]}
                            )
        results = update_results(results, params, opt_results)
    results_df = pd.DataFrame.from_dict(results)
    results_df = pd.merge(df, results_df, on="id")

    return results_df

def main(exp_file, nude_save_file, b6_save_file):
    param_bounds = {
        "n": [40,60],
        "init_totalPop": [16,24],
        "init_growVal": [0,0.5]
    }
    opt_bounds = [(0, 1)]

    all_results = pd.DataFrame()
    for i in range(50):
        print(i)
        params = {
            "n": round(np.random.uniform(param_bounds["n"][0], param_bounds["n"][1])),
            "init_totalPop": round(np.random.uniform(param_bounds["init_totalPop"][0], param_bounds["init_totalPop"][1])),
            "init_growVal": np.random.uniform(param_bounds["init_growVal"][0], param_bounds["init_growVal"][1]),
            "bounds": opt_bounds
        }
        curr_results = one_run(exp_file, params)
        
        curr_results["rep"] = i
        all_results = pd.concat([all_results, curr_results], ignore_index=True)

    nude = all_results[(all_results["exp"] == "Grp. B1 nude (100% C1)") | (all_results["exp"] == "Grp. B5 nude (100% C11)")]
    b6 = all_results[(all_results["exp"] == "Grp. A1 B6 (100% C1)") | (all_results["exp"] == "Grp. A5 B6 (100% C11)")]

    nude.to_csv(nude_save_file, index=False)
    b6.to_csv(b6_save_file, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--exp_file", action="store", default="results/growth_fit_results/exp_growth.csv")
    parser.add_argument("--nude_save_file", action="store", default="results/method5/nude_clone_growth_rates.csv")
    parser.add_argument("--b6_save_file", action="store", default="results/method5/b6_clone_growth_rates.csv")
    args = parser.parse_args()
    main(args.exp_file, args.nude_save_file, args.b6_save_file)