import pandas as pd
import numpy as np

data_file = "data/growth_data_orig.csv"
save_file = "data/growth_data_df.csv"

growth = []
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
        for i in range(len(data)):
            growth += [[group, tid, days[i], data[i]]]
df = pd.DataFrame(data=growth, columns=["group", "id", "day", "size"])
df.to_csv(save_file, index=False)