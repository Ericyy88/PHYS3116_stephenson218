import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data1 = pd.read_csv("data/HarrisPartI.csv")
data2 = pd.read_csv("data/HarrisPartIII.csv")

#define x and y values
x = data1["R_gc"]                                     #defining x as the metallicity values from the data
y = data2["v_LSR"]   
data = pd.merge(
    data1[["ID", "Name", "R_gc"]],
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

data["abs_v"] = data["v_LSR"].abs() 
suspect = data[
    ["ID", "Name", "v_LSR", "R_gc", "abs_v"]
]                                                           #variables of outliers table
suspect = suspect.sort_values("abs_v", ascending=False)   #sorting data by decending order of absolute standardized residuals
print(suspect.head(10))                                    #showing the 10 largest outliers in the data


outlier = data[data['abs_v'] > 2].copy()
outlier[['ID']].to_csv("outlier_clusters.csv", index=False)

plt.show()                  