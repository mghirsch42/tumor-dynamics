import pandas as pd

clone_growth_df = pd.read_csv("results/simple_model_2/clone_growth_rates.csv")

gb = clone_growth_df.groupby("exp")["est_growVal"].median().reset_index()
print("Medians by Experiment")
print(gb)

# gb = clone_growth_df.groupby(["exp", "id"])["est_growVal"].median().reset_index()
# print("Medians by ID")
# print(gb)