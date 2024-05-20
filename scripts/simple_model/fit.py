import numpy as np
from scipy.optimize import dual_annealing
import pandas as pd
import argparse
import utils

##########
# Calculates the base growth rate of the subline using the experiments with 
# only one subline in the nude mice
##########

def update_results(curr_results, params, n, opt_results):
    curr_results["exp"].append(params["exp"])
    curr_results["id"].append(params["id"])
    curr_results["n"].append(n)
    curr_results["init_totalPop"].append(params["init_totalPop"])
    curr_results["init_growVal"].append(params["init_growVal"])
    curr_results["est_growVal"].append(opt_results.x[0])
    curr_results["bounds"].append(params["bounds"])
    curr_results["obj_func_val"].append(opt_results.fun)
    return curr_results

def one_run(exp_file, params):
    # print(params)

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
        exp = row.name
        print(exp, row["id"])
        true_exp_params = {"a": row["a"], "b": row["b"], "c": row["c"]}
        params.update({"exp": exp, "id": row["id"]})
        if row["last_day"] > 50:
            n = int(row["last_day"] + params["n"])
        else:
            n = 50 + params["n"]

        opt_results = dual_annealing(utils.one_step_error_pure,
                            x0 = [params["init_growVal"]],
                            args = (n, params["init_totalPop"], true_exp_params),
                            bounds = params["bounds"],
                            minimizer_kwargs={"method": "L-BFGS-B", "bounds": params["bounds"]}
                            )

        results = update_results(results, params, n, opt_results)

    results_df = pd.DataFrame.from_dict(results)
    results_df = pd.merge(df, results_df, on="id")
    # print(results_df)
    return results_df

def main(exp_file, save_file):
    param_bounds = {
        "n": [-5, 5],
        "init_totalPop": [20,30],
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
    print(all_results)
    all_results.to_csv(save_file, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--exp_file", action="store", default="results/growth_fit_results/exp_growth.csv")
    parser.add_argument("--save_file", action="store", default="results/simple_model_3/clone_growth_rates.csv")
    args = parser.parse_args()
    main(args.exp_file, args.save_file)