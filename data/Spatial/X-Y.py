import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv("data/HarrisPartI.csv")
outer = pd.read_csv("data/outer_gcs.csv")

x = data["X"]                                    
y = data["Y"]   

fig, ax = plt.subplots(figsize=(8, 5))

ax.scatter(x, y, s=25, alpha=0.7)
ax.set_xlabel("X (kpc)")
ax.set_ylabel("Y (kpc)")
ax.set_title("Spatial Distribution of Globular Clusters")
ax.grid(alpha=0.25)

ax.scatter(
    outer["X"],
    outer["Y"],
    s=80,
    marker="x",
    label="Outer/Halo Candidates"
)

ax.scatter(0, 0, marker="+", s=100, label="Galactic Centre")

ax.legend()
plt.show()