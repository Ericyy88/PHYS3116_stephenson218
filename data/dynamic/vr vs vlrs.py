import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv("data/HarrisPartIII.csv")

#define x and y values
x = data["v_r"]                                   
y = data["v_LSR"]   

fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(data["v_r"], data["v_LSR"], color="navy", s=20, alpha=0.7)
ax.set_xlabel("v_r (km/s)")
ax.set_ylabel("v_LSR (km/s)")
ax.set_title("Velocity vs Radial Velocity of Clusters")
ax.grid(alpha = 0.25)


plt.show()