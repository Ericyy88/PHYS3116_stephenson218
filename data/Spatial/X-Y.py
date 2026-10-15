
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load datasets
data = pd.read_csv("data/HarrisPartI_standardized.csv")
outer = pd.read_csv("Spatial_outliers.csv")

# Standardise cluster names
data["ID"] = data["ID"].astype(str).str.strip()
outer["ID"] = outer["ID"].astype(str).str.strip()

# Retrieve X and Y coordinates for outliers
outer = pd.merge(
    outer[["ID"]],
    data[["ID", "X", "Y"]],
    on="ID",
    how="inner"
)

# Plot all globular clusters
fig, ax = plt.subplots(figsize=(8, 5))

ax.scatter(
    data["X"],
    data["Y"],
    s=25,
    alpha=0.7,
    label="All Globular Clusters"
)

# Highlight spatial outliers
ax.scatter(
    outer["X"],
    outer["Y"],
    s=80,
    marker="x",
    color="red",
    label="Spatial Outliers"
)

# Galactic centre
ax.scatter(
    0, 0,
    marker="+",
    s=100,
    color="black",
    label="Galactic Centre"
)

ax.set_xlabel("X (kpc)")
ax.set_ylabel("Y (kpc)")
ax.set_title("Spatial Distribution of Globular Clusters")
ax.grid(alpha=0.25)
ax.legend()

plt.tight_layout()
plt.show()
