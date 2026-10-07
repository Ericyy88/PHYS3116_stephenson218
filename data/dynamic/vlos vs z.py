import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data1 = pd.read_csv("data/HarrisPartI.csv")
data2 = pd.read_csv("data/HarrisPartIII.csv")

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

plt.show()