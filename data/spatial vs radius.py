import pandas as pd
import matplotlib.pyplot as plt

# Read data
data1 = pd.read_csv("data/HarrisPartI.csv")
data2 = pd.read_csv("data/HarrisPartIII.csv")

# Merge the two Harris tables using cluster ID
data = pd.merge(
    data1[["ID", "Name", "R_gc", "Z"]],
    data2[["ID", "v_LSR"]],
    on="ID",
    how="inner"
)

# Remove rows missing any of the variables we need
data = data.dropna(
    subset=["Z", "v_LSR", "R_gc"]
)

# Create figure
fig, ax = plt.subplots(figsize=(9, 6))

# Scatter plot:
# x = vertical position
# y = radial velocity
# colour = galactocentric radius
scatter = ax.scatter(
    data["Z"],
    data["v_LSR"],
    c=data["R_gc"],
    s=35,
    alpha=0.8
)

# Axis labels
ax.set_xlabel("Z (kpc)")
ax.set_ylabel("v_LSR (km/s)")

ax.set_title(
    "Velocity vs Vertical Position of Globular Clusters"
)

ax.grid(alpha=0.25)

# Colour bar showing R_gc
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label("R_gc (kpc)")

plt.tight_layout()
plt.show()