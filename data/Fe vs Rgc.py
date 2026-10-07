import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data1 = pd.read_csv("data/vandenBerg_table2.csv")
data2 = pd.read_csv("data/HarrisPartI.csv")
outliers = pd.read_csv("outlier_clusters.csv")

#define x and y values
x = data1["FeH"]                                     #defining x as the metallicity values from the data
y = data2["R_gc"]   

data = pd.merge(
    x,
    y,
    left_index=True,
    right_index=True
)                                  #defining y as the galactocentric radius values from the data

#Plotting metallicity vs galactocentric radius
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(data["R_gc"], data["FeH"], color="navy", s=20, alpha=0.7)
ax.set_xlabel("R_gc (kpc)")
ax.set_ylabel("[Fe/H]")
ax.set_title("Metallicity vs Galactocentric Radius of Clusters")
ax.grid(alpha = 0.25)
plt.show()