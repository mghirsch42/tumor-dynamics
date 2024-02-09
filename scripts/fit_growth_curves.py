import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score
import pandas as pd
import argparse
import json
import utils

##########
# Estimate basic function parameters based on the true data, one for each experiment
##########


def main(data_file, save_file):
    params = {
        "init_a": 20,
        "init_b": .1,
        "init_c": 20,
        "bounds_a": [0, np.inf],
        "bounds_b": [0, np.inf],
        "bounds_c": [10, 35]
    }

    growth = []
    days = []

    # Read the data
    with open(data_file, "r") as f:
        for line in f.readlines():
            line = line.strip().split(",")
            # header
            if line[0] == "Group":
                days = np.asarray(line[2:], dtype=np.int64)
                continue
            # data
            line = list(filter(None, line))
            group = line[0]
            tid = line[1]
            data = list(map(float, line[2:]))
            growth += [[group, tid, data]]
    # print(growth)

    results = []
    # Loop through each experiment
    for row in growth:
        print(row)
        ydata = row[2]
        xdata = days[0:len(ydata)]
        popt, pcov = curve_fit(utils.exp_funct, xdata, ydata, 
                        p0=(params["init_a"], params["init_b"], params["init_c"]), 
                        bounds=([params["bounds_a"][0], params["bounds_b"][0], params["bounds_c"][0]], 
                                [params["bounds_a"][1], params["bounds_b"][1], params["bounds_c"][1]]))
        opt_line = [utils.exp_funct(x, popt[0], popt[1], popt[2]) for x in xdata]
        r = r2_score(ydata, opt_line)
        results.append([row[0], row[1]] + list(popt) + [r])

    cols = ["group", "id", "a", "b", "c", "rscore"]
    df = pd.DataFrame(results, columns=cols)
    df = df[df["id"] != 438] # Exclude the weird one
    print(df)
    df.to_csv(save_file, index=False)
    
    # Save parameters
    with open(save_file.split(".")[0]+"_params.json", "w") as f:
        f.write(json.dumps(params, indent=4))
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--data_file", type=str, action="store", default="data/growth_data.csv")
    parser.add_argument("-s", "--save_file", type=str, action="store", default="results/growth_fit_results/exp_growth.csv")
    args = parser.parse_args()
    main(args.data_file, args.save_file)