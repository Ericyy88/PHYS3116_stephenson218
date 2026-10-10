import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data1 = pd.read_csv("data/HarrisPartI_standardized.csv")
data2 = pd.read_csv("data/HarrisPartIII_standardized.csv")

#define x and y values
x = data1["R_gc"]                                     #defining x as the metallicity values from the data
y = data2["v_LSR"]   
data = pd.merge(
    data1[["ID", "R_gc"]],
    data2[["ID", "v_LSR"]],
    on="ID",
    how="inner"
)
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(data["R_gc"], data["v_LSR"], color="navy", s=20, alpha=0.7)
ax.set_xlabel("R_gc (kpc)")
ax.set_ylabel("v_LSR (km/s)")
ax.set_title("Velocity vs Galactocentric Radius of Clusters")
ax.grid(alpha = 0.25)


# Calculate absolute velocity
data["abs_v"] = data["v_LSR"].abs()

# Rank clusters by absolute velocity
ranked = data.sort_values("abs_v", ascending=False)

# Select top 20 velocity outliers
velocity_outliers = ranked.head(20).copy()

print("\nTop 20 Velocity Outliers:")
print(velocity_outliers[
    ["ID", "v_LSR", "R_gc", "abs_v"]
].to_string(index=False))

# Save top 20 cluster IDs
velocity_outliers[["ID"]].to_csv(
    "Velocity_outliers.csv", index=False
)


plt.show()     


