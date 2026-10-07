import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv("data/HarrisPartI.csv")

x = data["Z"]                                    
y = data["R_gc"]   

fig, ax = plt.subplots(figsize=(8, 5))

ax.scatter(x, y, s=25, alpha=0.7)
ax.set_xlabel("Z (kpc)")
ax.set_ylabel("R_gc (kpc)")
ax.set_title("Vertical Distribution of Globular Clusters")
ax.grid(alpha=0.25)

ax.scatter(0, 0, marker="x", s=100, label="Galactic Centre")

outer = data[
    (data["R_gc"] > 30) |
    (np.abs(data["Z"]) > 20)
]

outer.to_csv("data/outer_gcs.csv", index=False)


print(outer[["ID", "Name", "R_gc", "X", "Y", "Z"]])

ax.legend()
plt.show()