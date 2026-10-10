
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from scipy.stats import mannwhitneyu

# Import datasets
data1 = pd.read_csv("data/vandenBerg_table2_standardized.csv")
data2 = pd.read_csv("data/HarrisPartI_standardized.csv")
data3 = pd.read_csv("data/HarrisPartIII_standardized.csv")

# Import previously identified velocity outliers
velocity_outliers = pd.read_csv("Velocity_outliers.csv")

# Merge datasets
data = pd.merge(
    data1[["ID", "Age", "Age_err", "FeH"]],
    data2[["ID", "R_gc"]],
    on="ID",
    how="inner"
)

data = pd.merge(
    data,
    data3[["ID", "v_LSR"]],
    on="ID",
    how="inner"
)

# Remove missing values
data = data.dropna(
    subset=["Age", "FeH", "R_gc", "v_LSR"]
).copy()

# Identify velocity outliers
data["velocity_outlier"] = data["ID"].isin(
    velocity_outliers["ID"]
)

# Plot
fig, ax = plt.subplots(figsize=(9, 6))

sc = ax.scatter(
    data["FeH"],
    data["Age"],
    c=data["R_gc"],
    cmap="viridis",
    s=40,
    alpha=0.85
)

# Age uncertainties
ax.errorbar(
    data["FeH"],
    data["Age"],
    yerr=data["Age_err"],
    fmt="none",
    ecolor="lightgray",
    capsize=2,
    zorder=0
)

# Highlight velocity outliers
outliers = data[data["velocity_outlier"]]

ax.scatter(
    outliers["FeH"],
    outliers["Age"],
    facecolors="none",
    edgecolors="red",
    s=110,
    linewidths=1.7,
    label="High |v_LSR| clusters"
)

# Label highlighted clusters
for _, row in outliers.iterrows():
    ax.annotate(
        row["ID"],
        (row["FeH"], row["Age"]),
        xytext=(5, 5),
        textcoords="offset points",
        fontsize=8
    )

# Colour bar
cbar = plt.colorbar(sc, ax=ax)
cbar.set_label("Galactocentric Distance (kpc)")

ax.set_xlabel("[Fe/H]")
ax.set_ylabel("Age (Gyr)")
ax.set_title("Age vs Metallicity by Galactocentric Distance")
ax.grid(alpha=0.25)
ax.legend()


data["age_outlier"] = data["ID"].isin(
    pd.read_csv("Age_outliers.csv")["ID"]
)

fig, ax = plt.subplots(figsize=(7, 5))

ax.boxplot(
    [
        data.loc[~data["age_outlier"], "R_gc"],
        data.loc[data["age_outlier"], "R_gc"]
    ],
    tick_labels=["Other clusters", "Age outliers"]
)

ax.set_ylabel("Galactocentric Distance (kpc)")
ax.set_title("Galactocentric Distance by Age-Metallicity Group")
ax.grid(axis="y", alpha=0.25)



normal = data.loc[~data["age_outlier"], "R_gc"]
outliers = data.loc[data["age_outlier"], "R_gc"]

stat, p = mannwhitneyu(
    normal,
    outliers,
    alternative="two-sided"
)

print("Mann–Whitney U:", stat)
print("p-value:", p)

plt.show()


plt.tight_layout()
plt.show()

print("Clusters after merge:", len(data))
print("Highlighted velocity outliers:", len(outliers))
