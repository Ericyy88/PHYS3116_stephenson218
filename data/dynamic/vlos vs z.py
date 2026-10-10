import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data1 = pd.read_csv("data/HarrisPartI_standardized.csv")
data2 = pd.read_csv("data/HarrisPartIII_standardized.csv")

#define x and y values
x = data1["Z"]                                   
y = data2["v_LSR"]   
data = pd.merge(
    data1[["ID", "Name", "Z"]],
    data2[["ID", "v_LSR"]],
    on="ID",
    how="inner"
)
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(data["Z"], data["v_LSR"], color="navy", s=20, alpha=0.7)
ax.set_xlabel("Z (kpc)")
ax.set_ylabel("v_LSR (km/s)")
ax.set_title("Velocity vs Vertical Position of Clusters")
ax.grid(alpha = 0.25)


# Calculate absolute velocity
data["abs_z"] = data["Z"].abs()

# Rank clusters by absolute velocity
ranked = data.sort_values("abs_z", ascending=False)

# Select top 20 velocity outliers
velocity_outliers = ranked.head(20).copy()

print("\nTop 20 Velocity Outliers:")
print(velocity_outliers[
    ["ID", "v_LSR", "Z", "abs_z"]
].to_string(index=False))

# Save top 20 cluster IDs
velocity_outliers[["ID"]].to_csv(
    "vLSR_z_outliers.csv", index=False
)

plt.show()

