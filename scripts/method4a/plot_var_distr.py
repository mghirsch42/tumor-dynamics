import pandas as pd
from matplotlib import pyplot as plt
from utils import get_id_colors

clone_growth_df = pd.read_csv("results/method4a/clone_growth_rates.csv")
clone_intr_df = pd.read_csv("results/method4a/clone_interaction.csv")
t_intr_df = pd.read_csv("results/method4a/t_interaction.csv")
title_prefix = "Method 4a"
save_path = "figures/method4a/"

show = True
save = True

clone_growth_df = clone_growth_df.sort_values(["exp", "id"])
clone_intr_df = clone_intr_df.sort_values(["exp", "id"])
t_intr_df = t_intr_df.sort_values(["exp", "id"])

id_colors = get_id_colors()

# 1. Plot clone growth rates
r_growth = clone_growth_df[clone_growth_df["exp"] == "Grp. B5 nude (100% C11)"]
plt.figure()
for id in r_growth["id"].unique():
    plt.hist(r_growth[r_growth["id"] == id]["est_growVal"], label=id, alpha=0.75, color=id_colors[id])
# plt.hist(r_growth["est_growVal"], label=id)#, alpha=0.75)
plt.title(title_prefix + "\nR growth rate")
plt.legend()
if save:
    plt.savefig(save_path+"growR.png")
if show:
    plt.show()
plt.close()
# exit()

s_growth = clone_growth_df[clone_growth_df["exp"] == "Grp. B1 nude (100% C1)"]
plt.figure()
for id in s_growth["id"].unique():
    plt.hist(s_growth[s_growth["id"] == id]["est_growVal"], label=id, alpha=0.75, color=id_colors[id])
# plt.hist(s_growth["est_growVal"], label=id)#, alpha=0.75)
plt.title(title_prefix + "\nS growth rate")
plt.legend()
if save:
    plt.savefig(save_path+"growS.png")
if show:
    plt.show()
plt.close()

# 2. Plot clone interaction terms
plt.figure()
plt.hist(clone_intr_df["est_intrRS"])
plt.title(title_prefix + "\nInfluence of S on R")
if save:
    plt.savefig(save_path+"intrRS.png")
if show:
    plt.show()
plt.close()

plt.figure()
plt.hist(clone_intr_df["est_intrSR"])
plt.title(title_prefix + "\nInfluence of R on S")
if save:
    plt.savefig(save_path+"intrSR.png")
if show:
    plt.show()
plt.close()

# 3. Plot T-cell interaction terms
t_pure_df = t_intr_df[(t_intr_df["exp"] == "Grp. A1 B6 (100% C1)") | (t_intr_df["exp"] == "Grp. A5 B6 (100% C11)")]
t_intr_df = t_intr_df[(t_intr_df["exp"] != "Grp. A1 B6 (100% C1)") & (t_intr_df["exp"] != "Grp. A5 B6 (100% C11)")]

# exit()
plt.figure()
plt.hist(t_intr_df["est_intrRT"], label="admix")
plt.hist(t_pure_df[t_pure_df["exp"]=="Grp. A5 B6 (100% C11)"]["est_intrRT"], label="pure", alpha= 0.75)
plt.title(title_prefix + "\nInfluence of T on R")
plt.legend()
if save:
    plt.savefig(save_path+"intrRT.png")
if show:
    plt.show()
plt.close()

plt.hist(t_intr_df["est_intrST"], label="admix")
plt.hist(t_pure_df[t_pure_df["exp"]=="Grp. A1 B6 (100% C1)"]["est_intrST"], label="pure", alpha=0.75)
plt.title(title_prefix + "\nInfluence of T on S")
plt.legend()
if save:
    plt.savefig(save_path+"intrST.png")
if show:
    plt.show()
plt.close()

plt.figure()
plt.hist(t_intr_df["est_intrTV"], label="admix")
plt.hist(t_pure_df["est_intrTV"], label="pure", alpha=0.75)
plt.title(title_prefix + "\nInfluence of tumor on T")
plt.legend()
if save:
    plt.savefig(save_path+"intrTV.png")
if show:
    plt.show()
plt.close()