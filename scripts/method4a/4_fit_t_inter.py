import numpy as np
from scipy.optimize import dual_annealing
import pandas as pd
import argparse
import utils


def update_results(curr_results, params, opt_results):
    curr_results["exp"].append(params["exp"])
    curr_results["id"].append(params["id"])
    curr_results["n"].append(params["n"])
    curr_results["init_totalPop"].append(params["init_totalPop"])
    curr_results["initR"].append(params["initR"])
    curr_results["initS"].append(params["initS"])
    curr_results["initT"].append(params["initT"])
    curr_results["avg_growR"].append(params["avg_growR"])
    curr_results["avg_growS"].append(params["avg_growS"])
    curr_results["avg_intrRS"].append(params["avg_intrRS"])
    curr_results["avg_intrSR"].append(params["avg_intrSR"])
    curr_results["bounds"].append(params["bounds"])
    curr_results["init_intrRT"].append(params["init_intrRT"])
    curr_results["init_intrST"].append(params["init_intrST"])
    curr_results["init_intrTV"].append(params["init_intrTV"])
    curr_results["est_intrRT"].append(opt_results.x[0])
    curr_results["est_intrST"].append(opt_results.x[1])
    curr_results["est_intrTV"].append(opt_results.x[2])
    curr_results["obj_func_val"].append(opt_results.fun)
    return curr_results

def one_run(exp_file, clone_intr_file, t_intr_pure_file, t_init_file, params):

    results = {
        "exp": [],
        "id": [],
        "n": [],
        "init_totalPop": [],
        "initR": [],
        "initS": [],
        "initT": [],
        "avg_growR": [],
        "avg_growS": [],
        "avg_intrRS": [],
        "avg_intrSR": [],
        "init_intrRT": [],
        "init_intrST": [],
        "init_intrTV": [],
        "bounds": [],
        "est_intrRT": [],
        "est_intrST": [],
        "est_intrTV": [],
        "obj_func_val": [],
    }

    df = pd.read_csv(exp_file, index_col=0)
    clone_intr_df = pd.read_csv(clone_intr_file)
    t_init_df = pd.read_csv(t_init_file)
    params.update({"avg_growR": clone_intr_df.loc[0,"avg_growR"], "avg_growS": clone_intr_df.loc[0,"avg_growS"]})
    avg_intrRS = clone_intr_df["est_intrRS"].mean()
    avg_intrSR = clone_intr_df["est_intrSR"].mean()
    params.update({"avg_intrRS": avg_intrRS, "avg_intrSR": avg_intrSR})

    for idx, row in df.iterrows():
        if not "B6" in row.name: continue # Only use standard mice
        if "A1" in row.name or "A5" in row.name: continue # Skip the pure experiments
        if row["id"] == 438: continue # This experiment is bad

        exp = row.name
        print(exp)
        true_exp_params = {"a": row["a"], "b": row["b"], "c": row["c"]}
        params.update({"exp": exp, "id": row["id"]})
        params.update(utils.get_init_R_S(params["init_totalPop"], exp))
        
        grow_vals = {"avg_growR": params["avg_growR"], "avg_growS": params["avg_growS"]}
        params.update({"initT": params["init_totalPop"]*t_init_df[t_init_df["Exp"] == exp].reset_index().loc[0,"T_round"]})

        init_pop_vals = {"initR": params["initR"], "initS": params["initS"], "initT": params["initT"]}
        intr_vals = {"avg_intrRS": params["avg_intrRS"], "avg_intrSR": params["avg_intrSR"]}

        opt_results = dual_annealing(utils.one_step_error_t,
                        x0 = [params["init_intrRT"], params["init_intrST"], params["init_intrTV"]],
                        args = (params["n"], grow_vals, init_pop_vals, intr_vals, true_exp_params),
                        bounds = params["bounds"],
                        minimizer_kwargs={"method": "L-BFGS-B", "bounds": params["bounds"]}
                        )
        
        results = update_results(results, params, opt_results)
        
    results_df = pd.DataFrame.from_dict(results)
    results_df = pd.merge(df, results_df, on="id")
    return results_df

def main(exp_file, clone_intr_file, t_intr_pure_file, t_init_file, save_file):
    param_bounds = {
        "n": [40, 60],
        "init_totalPop": [16,24],
        "init_intrRT": [-0.1, 0.1],
        "init_intrST": [-0.1, 0.1],
        "init_intrTV": [-0.1, 0.1],
    }
    opt_bounds =  ((-.5, .5), (-.5, .5), (-.5, .5))

    all_results = pd.DataFrame()
    for i in range(50):
        print(i)
        params = {
            "n": round(np.random.uniform(param_bounds["n"][0], param_bounds["n"][1])),
            "init_totalPop": round(np.random.uniform(param_bounds["init_totalPop"][0], param_bounds["init_totalPop"][1])),
            "init_intrRT": np.random.uniform(param_bounds["init_intrRT"][0], param_bounds["init_intrRT"][1]),
            "init_intrST": np.random.uniform(param_bounds["init_intrST"][0], param_bounds["init_intrST"][1]),
            "init_intrTV": np.random.uniform(param_bounds["init_intrTV"][0], param_bounds["init_intrTV"][1]),
            "bounds": opt_bounds
        }
        curr_results = one_run(exp_file, clone_intr_file, t_intr_pure_file, t_init_file, params)
        curr_results["rep"] = i
        all_results = pd.concat([all_results, curr_results], ignore_index=True)
    pure_results = pd.read_csv(t_intr_pure_file)
    all_results = pd.concat([pure_results, all_results])
    all_results.to_csv(save_file, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--exp_file", action="store", default="results/growth_fit_results/exp_growth.csv")
    parser.add_argument("--clone_intr_file", action="store", default="results/method4a/clone_interaction.csv")
    parser.add_argument("--t_intr_pure_file", action="store", default="results/method4a/t_interaction_pure.csv")
    parser.add_argument("--t_init_file", action="store", default="data/t_cell_starting_sizes.csv")
    parser.add_argument("--save_file", action="store", default="results/method4a/t_interaction.csv")
    args = parser.parse_args()
    main(args.exp_file, args.clone_intr_file, args.t_intr_pure_file, args.t_init_file, args.save_file)
