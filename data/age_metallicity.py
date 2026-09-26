import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("vandenBerg_table2.csv")

#Plotting age vs cluster 
fig, ax = plt.subplots(figsize=(8, 5))
#uncertainties
ax.errorbar(
    data["FeH"],
    data["Age"],
    yerr = data["Age_err"],
    fmt = "o",
    markersize = 4,
    capsize = 3,
    color = "navy",
    ecolor = "lightgray",
    elinewidth = 1,
)

ax.set_xlabel("[Fe/H]")
ax.set_ylabel("Age (Gyr)")
ax.set_title("Age vs Metallicity of Clusters")
ax.grid(alpha = 0.25)
plt.show()