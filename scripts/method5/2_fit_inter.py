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

def one_run(exp_file, growth_rate_file, mouse_type, params):
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
    if mouse_type == "nude":
        avg_growR = growth_rate_df[growth_rate_df["exp"].str.contains("B5")]["est_growVal"].median()
        avg_growS = growth_rate_df[growth_rate_df["exp"].str.contains("B1")]["est_growVal"].median()
    else:
        avg_growR = growth_rate_df[growth_rate_df["exp"].str.contains("A5")]["est_growVal"].median()
        avg_growS = growth_rate_df[growth_rate_df["exp"].str.contains("A1")]["est_growVal"].median()
    params.update({"avg_growR": avg_growR, "avg_growS": avg_growS})

    for idx, row in df.iterrows():
        if mouse_type == "nude":
            if not("B2" in row.name or "B3" in row.name or "B4" in row.name): continue 
        else:
            if not("A2" in row.name or "A3" in row.name or "A4" in row.name): continue
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

def main(exp_file, nude_growth_rate_file, b6_growth_rate_file, nude_save_file, b6_save_file):
    param_bounds = {
        "n": [40, 60],
        "init_totalPop": [16,24],
        "init_intrRS": [-0.1, 0.1],
        "init_intrSR": [-0.1, 0.1],
    }
    opt_bounds = ((-.5, .5), (-.5, .5))

    nude_all_results = pd.DataFrame()
    b6_all_results = pd.DataFrame()
    for i in range(50):
        print(i)
        params = {
            "n": round(np.random.uniform(param_bounds["n"][0], param_bounds["n"][1])),
            "init_totalPop": round(np.random.uniform(param_bounds["init_totalPop"][0], param_bounds["init_totalPop"][1])),
            "init_intrRS": np.random.uniform(param_bounds["init_intrRS"][0], param_bounds["init_intrRS"][1]),
            "init_intrSR": np.random.uniform(param_bounds["init_intrSR"][0], param_bounds["init_intrSR"][1]),
            "bounds": opt_bounds
        }
        nude_curr_results = one_run(exp_file, nude_growth_rate_file, "nude", params)
        nude_curr_results["rep"] = i
        nude_all_results = pd.concat([nude_all_results, nude_curr_results], ignore_index=True)
        
        b6_curr_results = one_run(exp_file, b6_growth_rate_file, "b6", params)
        b6_curr_results["rep"] = i
        b6_all_results = pd.concat([b6_all_results, b6_curr_results], ignore_index=True)
        
    nude_all_results.to_csv(nude_save_file, index=False)
    b6_all_results.to_csv(b6_save_file, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--exp_file", action="store", default="results/growth_fit_results/exp_growth.csv")
    parser.add_argument("--nude_growth_rate_file", action="store", default="results/method5/nude_clone_growth_rates.csv")
    parser.add_argument("--b6_growth_rate_file", action="store", default="results/method5/b6_clone_growth_rates.csv")
    parser.add_argument("--nude_save_file", action="store", default="results/method5b/nude_clone_interaction.csv")
    parser.add_argument("--b6_save_file", action="store", default="results/method5b/b6_clone_interaction.csv")
    args = parser.parse_args()
    main(args.exp_file, args.nude_growth_rate_file, args.b6_growth_rate_file, args.nude_save_file, args.b6_save_file)
