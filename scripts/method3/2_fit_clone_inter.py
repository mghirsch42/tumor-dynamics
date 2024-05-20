import numpy as np
from scipy.optimize import dual_annealing
import pandas as pd
import argparse
import utils

##########
# Estimates the interaction between sublines using the mean estimated growth rates and nude mice
##########

def update_results(curr_results, params, opt_results):
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

def one_run(exp_file, growth_rate_file, params):

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
                        minimizer_kwargs={"method": "L-BFGS-B", "bounds": params["bounds"]}
                        )
        
        results = update_results(results, params, opt_results)
    results_df = pd.DataFrame.from_dict(results)
    results_df = pd.merge(df, results_df, on="id")
    return results_df

def main(exp_file, growth_rate_file, save_file):
    param_bounds = {
        "n": [40, 60],
        "init_totalPop": [16,24],
        "init_intrRS": [-0.1, 0.1],
        "init_intrSR": [-0.1, 0.1],
    }
    opt_bounds = ((-.5, .5), (-.5, .5))

    all_results = pd.DataFrame()
    for i in range(50):
        print(i)
        params = {
            "n": round(np.random.uniform(param_bounds["n"][0], param_bounds["n"][1])),
            "init_totalPop": round(np.random.uniform(param_bounds["init_totalPop"][0], param_bounds["init_totalPop"][1])),
            "init_intrRS": np.random.uniform(param_bounds["init_intrRS"][0], param_bounds["init_intrRS"][1]),
            "init_intrSR": np.random.uniform(param_bounds["init_intrSR"][0], param_bounds["init_intrSR"][1]),
            "bounds": opt_bounds
        }
        curr_results = one_run(exp_file, growth_rate_file, params)
        curr_results["rep"] = i
        all_results = pd.concat([all_results, curr_results], ignore_index=True)
    all_results.to_csv(save_file, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--exp_file", action="store", default="results/growth_fit_results/exp_growth.csv")
    parser.add_argument("--growth_rate_file", action="store", default="results/method3/clone_growth_rates.csv")
    parser.add_argument("--save_file", action="store", default="results/method3/clone_interaction.csv")
    args = parser.parse_args()
    main(args.exp_file, args.growth_rate_file, args.save_file)
