import pandas as pd
from matplotlib import colormaps
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns

df = pd.read_csv("results/method4a/t_interaction.csv")
rs_df = pd.read_csv("results/method4a/clone_interaction.csv")
save_path = "figures/interaction_figures/method4a/"

rt_df = df[["exp", "id", "est_intrRT", "est_intrTV"]]
st_df = df[["exp", "id", "est_intrST", "est_intrTV"]]

rt_df = rt_df.dropna()
st_df = st_df.dropna()
rs_df = rs_df.dropna()
rt_df_avg = rt_df.groupby(["exp", "id"]).mean().reset_index()
st_df_avg = st_df.groupby(["exp", "id"]).mean().reset_index()
rs_df_avg = rs_df.groupby(["exp", "id"])[["est_intrRS", "est_intrSR"]].mean().reset_index()

color_list = colormaps["tab20"].colors


# Heatmaps
fig, axes = plt.subplots(nrows=1, ncols=4)
exps = rt_df_avg["exp"].unique()
cbar = False
for i in range(len(exps)):
    exp_data = rt_df_avg[rt_df_avg["exp"]==exps[i]]
    if i == len(exps)-1:
        cbar = True
    sns.heatmap(data=exp_data[["est_intrRT", "est_intrTR"]], ax=axes[i], annot=True, yticklabels=exp_data["id"], cbar=cbar)
    axes[i].set_title(exps[i])
plt.suptitle("R vs T")
plt.show()
plt.close()

fig, axes = plt.subplots(nrows=1, ncols=4)
exps = st_df_avg["exp"].unique()
cbar = False
for i in range(len(exps)):
    exp_data = st_df_avg[st_df_avg["exp"]==exps[i]]
    if i == len(exps)-1:
        cbar = True
    sns.heatmap(data=exp_data[["est_intrST", "est_intrTS"]], ax=axes[i], annot=True, yticklabels=exp_data["id"], cbar=cbar)
    axes[i].set_title(exps[i])
plt.suptitle("S vs T")
plt.show()
plt.close()
