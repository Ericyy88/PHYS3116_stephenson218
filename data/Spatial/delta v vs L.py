import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data1 = pd.read_csv("data/HarrisPartI.csv")
data2 = pd.read_csv("data/HarrisPartIII.csv")
  
data = pd.merge(
    data1[["ID", "Name", "L", "B"]],
    data2[["ID", "v_LSR", "v_r"]],
    on="ID",
    how="inner"
)
data["delta_v"] = data2["v_LSR"] - data2["v_r"]
fig, ax = plt.subplots(figsize=(8, 5))
sc = ax.scatter(
    data["L"],
    data["delta_v"],
    c=data["B"],
    s=30,
    alpha=0.8
)

ax.set_xlabel("L (degrees)")
ax.set_ylabel(r"$\delta v$ (km/s)")
ax.set_title("LSR Velocity Correction vs Galactic Longitude")
ax.grid(alpha=0.25)

cbar = plt.colorbar(sc, ax=ax)
cbar.set_label("B (degrees)")

plt.show()