from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# --------------------------------------------------
# 1. Import datasets
# --------------------------------------------------

folder = Path(__file__).resolve().parent

data = pd.read_csv(
    folder / "orbital_energy_angular_momentum.csv"
)

age_outliers = pd.read_csv(
    folder.parent.parent / "Age_outliers.csv"
)

velocity_outliers = pd.read_csv(
    folder.parent.parent / "Velocity_outliers.csv"
)

dispersion_outliers = pd.read_csv(
    folder.parent.parent / "Sig_v_outliers.csv"
)

# Standardise cluster identifiers
def standardise_id(series):
    return (
        series.astype(str)
        .str.upper()
        .str.strip()
        .str.replace(r"[\s_-]+", "", regex=True)
        .str.replace("DJORG", "DJOR", regex=False)
        .str.replace("2MASS", "2MS", regex=False)
    )

data["match_id"] = standardise_id(data["ID"])
age_outliers["match_id"] = standardise_id(age_outliers["ID"])
velocity_outliers["match_id"] = standardise_id(
    velocity_outliers["ID"]
)
dispersion_outliers["match_id"] = standardise_id(
    dispersion_outliers["ID"]
)

print("\nOrbital catalogue IDs:")
print(data["ID"].head(20).tolist())

print("\nAge outlier IDs:")
print(age_outliers["ID"].head(20).tolist())

print("\nVelocity dispersion outlier IDs:")
print(velocity_outliers["ID"].head(20).tolist())

print("\nVelocity dispersion outlier IDs:")
print(dispersion_outliers["ID"].head(20).tolist())
# --------------------------------------------------
# 2. Identify outlier groups
# --------------------------------------------------

age_ids = set(age_outliers["match_id"])
velocity_ids = set(velocity_outliers["match_id"])
dispersion_ids = set(dispersion_outliers["match_id"])

data["Age_outlier"] = data["match_id"].isin(age_ids)
data["Velocity_outlier"] = data["match_id"].isin(velocity_ids)
data["Dispersion_outlier"] = data["match_id"].isin(dispersion_ids)

# Number of outlier lists containing each cluster
data["Outlier_count"] = (
    data["Age_outlier"].astype(int)
    + data["Velocity_outlier"].astype(int)
    + data["Dispersion_outlier"].astype(int)
)

normal = data["Outlier_count"] == 0

age_only = (
    data["Age_outlier"]
    & (data["Outlier_count"] == 1)
)

velocity_only = (
    data["Velocity_outlier"]
    & (data["Outlier_count"] == 1)
)

dispersion_only = (
    data["Dispersion_outlier"]
    & (data["Outlier_count"] == 1)
)

two_groups = data["Outlier_count"] == 2
all_three = data["Outlier_count"] == 3

# --------------------------------------------------
# 3. Scale orbital variables
# --------------------------------------------------

data["Lz_scaled"] = data["Lz_kpc_km_s"] / 1000
data["E_scaled"] = data["E_km2_s2"] / 100000

# --------------------------------------------------
# 4. Plot orbital energy against angular momentum
# --------------------------------------------------

fig, ax = plt.subplots(figsize=(14, 9))

groups = [
    (normal, "Other clusters", "lightgray", "o", 30),
    (age_only, "Age-metallicity only", "royalblue", "o", 85),
    (velocity_only, "Velocity only", "tomato", "o", 85),
    (dispersion_only, "Dispersion only", "orange", "o", 85),
    (two_groups, "Two outlier groups", "purple", "D", 120),
    (all_three, "All three groups", "gold", "*", 200),
]

for mask, label, color, marker, size in groups:
    ax.scatter(
        data.loc[mask, "Lz_scaled"],
        data.loc[mask, "E_scaled"],
        s=size,
        color=color,
        marker=marker,
        edgecolors="black" if label != "Other clusters" else "none",
        linewidths=0.5,
        alpha=0.85,
        label=label,
        zorder=5 if label == "All three groups" else 3
    )

# --------------------------------------------------
# 5. Annotate all outlier clusters
# --------------------------------------------------

from adjustText import adjust_text

texts = []

outlier_data = data.loc[data["Outlier_count"] >= 1]

for _, row in outlier_data.iterrows():

    txt = ax.text(
        row["Lz_scaled"],
        row["E_scaled"],
        row["ID"],
        fontsize=8,
        fontweight="bold" if row["Outlier_count"] >= 2 else "normal",
        zorder=6
    )

    texts.append(txt)

adjust_text(
    texts,
    ax=ax,
    arrowprops=dict(
        arrowstyle="-",
        color="gray",
        lw=0.6
    )
)

# --------------------------------------------------
# 6. Formatting
# --------------------------------------------------

ax.axvline(
    0,
    color="gray",
    linestyle="--",
    linewidth=1
)

ax.set_xlabel(
    r"Specific angular momentum $L_z$ "
    r"[$10^3$ kpc km s$^{-1}$]"
)

ax.set_ylabel(
    r"Specific orbital energy $E$ "
    r"[$10^5$ km$^2$ s$^{-2}$]"
)

ax.set_title(
    "Orbital Energy vs Angular Momentum\n"
    "Age-Metallicity and Velocity Outliers"
)

ax.set_xlim(-3.7, 3.5)
ax.set_ylim(-2.85, -0.08)

ax.text(
    0.25, 1.01,
    "Prograde",
    transform=ax.transAxes,
    ha="center"
)

ax.text(
    0.75, 1.01,
    "Retrograde",
    transform=ax.transAxes,
    ha="center"
)

ax.grid(alpha=0.2)
ax.legend(loc="best")

plt.tight_layout()

# --------------------------------------------------
# 7. Print overlapping clusters
# --------------------------------------------------

print("\nClusters appearing in ALL THREE lists:")
print(
    data.loc[
        all_three,
        ["ID", "Lz_kpc_km_s", "E_km2_s2"]
    ].to_string(index=False)
)

print("\nClusters appearing in TWO lists:")
print(
    data.loc[
        two_groups,
        [
            "ID",
            "Age_outlier",
            "Velocity_outlier",
            "Dispersion_outlier"
        ]
    ].to_string(index=False)
)

print("\nNumber of clusters in each category:")
print(f"Normal: {normal.sum()}")
print(f"Age only: {age_only.sum()}")
print(f"Velocity only: {velocity_only.sum()}")
print(f"Dispersion only: {dispersion_only.sum()}")
print(f"Two groups: {two_groups.sum()}")
print(f"All three: {all_three.sum()}")

data.to_csv(
    folder / "Orbital_outlier_comparison.csv",
    index=False
)

fig.savefig(
    folder / "Orbital_outlier_comparison.png",
    dpi=240,
    bbox_inches="tight"
)

plt.show()