import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data1 = pd.read_csv("data/HarrisPartI.csv")
data2 = pd.read_csv("data/HarrisPartIII.csv")

#define x and y values
x = data1["R_gc"]                                     #defining x as the metallicity values from the data
y = data2["v_LSR"]   
data = pd.merge(
    x,
    y,
    left_index=True,
    right_index=True
)             
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(data["R_gc"], data["v_LSR"], color="navy", s=20, alpha=0.7)
ax.set_xlabel("R_gc (kpc)")
ax.set_ylabel("v_LSR (km/s)")
ax.set_title("Velocity vs Galactocentric Radius of Clusters")
ax.grid(alpha = 0.25)

plt.show()                  