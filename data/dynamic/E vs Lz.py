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

print("\nOrbital catalogue IDs:")
print(data["ID"].head(20).tolist())

print("\nAge outlier IDs:")
print(age_outliers["ID"].head(20).tolist())

print("\nVelocity dispersion outlier IDs:")
print(velocity_outliers["ID"].head(20).tolist())
# --------------------------------------------------
# 2. Identify outlier groups
# --------------------------------------------------

age_ids = set(age_outliers["match_id"])
velocity_ids = set(velocity_outliers["match_id"])

data["Age_outlier"] = data["match_id"].isin(age_ids)
data["Velocity_outlier"] = data["match_id"].isin(velocity_ids)

both = data["Age_outlier"] & data["Velocity_outlier"]
age_only = data["Age_outlier"] & ~data["Velocity_outlier"]
velocity_only = ~data["Age_outlier"] & data["Velocity_outlier"]
normal = ~data["Age_outlier"] & ~data["Velocity_outlier"]

# --------------------------------------------------
# 3. Scale orbital variables
# --------------------------------------------------

data["Lz_scaled"] = data["Lz_kpc_km_s"] / 1000
data["E_scaled"] = data["E_km2_s2"] / 100000

# --------------------------------------------------
# 4. Plot orbital energy against angular momentum
# --------------------------------------------------

fig, ax = plt.subplots(figsize=(12, 7))

# Normal clusters
ax.scatter(
    data.loc[normal, "Lz_scaled"],
    data.loc[normal, "E_scaled"],
    s=30,
    color="lightgray",
    alpha=0.6,
    label="Other clusters",
    zorder=1
)

# Age-metallicity outliers only
ax.scatter(
    data.loc[age_only, "Lz_scaled"],
    data.loc[age_only, "E_scaled"],
    s=85,
    color="royalblue",
    edgecolors="black",
    linewidths=0.5,
    label="Age-metallicity outliers",
    zorder=3
)

# Velocity outliers only
ax.scatter(
    data.loc[velocity_only, "Lz_scaled"],
    data.loc[velocity_only, "E_scaled"],
    s=85,
    color="tomato",
    edgecolors="black",
    linewidths=0.5,
    label="Velocity outliers",
    zorder=3
)

# Clusters appearing in BOTH lists
ax.scatter(
    data.loc[both, "Lz_scaled"],
    data.loc[both, "E_scaled"],
    s=170,
    marker="*",
    color="gold",
    edgecolors="black",
    linewidths=0.8,
    label="Both outlier groups",
    zorder=5
)

# --------------------------------------------------
# 5. Annotate overlapping clusters
# --------------------------------------------------

for _, row in data.loc[both].iterrows():

    ax.annotate(
        row["ID"],
        xy=(row["Lz_scaled"], row["E_scaled"]),
        xytext=(8, 8),
        textcoords="offset points",
        fontsize=9,
        arrowprops=dict(
            arrowstyle="-",
            color="gray",
            lw=0.7
        ),
        zorder=6
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

overlap_clusters = data.loc[
    both,
    ["ID", "Lz_kpc_km_s", "E_km2_s2"]
].copy()

print("\nClusters appearing in BOTH outlier lists:")
print(overlap_clusters.to_string(index=False))

print("\nNumber of clusters in each category:")
print(f"Normal: {normal.sum()}")
print(f"Age only: {age_only.sum()}")
print(f"Velocity only: {velocity_only.sum()}")
print(f"Both: {both.sum()}")

# Save classified orbital data
data.to_csv(
    folder / "Orbital_outlier_comparison.csv",
    index=False
)

# Save figure
fig.savefig(
    folder / "Orbital_outlier_comparison.png",
    dpi=240,
    bbox_inches="tight"
)

plt.show()