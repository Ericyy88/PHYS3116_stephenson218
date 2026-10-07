import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data1 = pd.read_csv("data/vandenBerg_table2.csv")
data2 = pd.read_csv("data/Krause21.csv")

# Create matching cluster IDs
data1["NGC_ID"] = "NGC" + data1["#NGC"].astype(str)
data2["NGC_ID"] = data2["Object"].str.replace(" ", "").str.upper()

# Merge VandenBerg age/metallicity with Krause stellar mass
data = pd.merge(
    data1[["NGC_ID", "Age", "FeH"]],
    data2[["NGC_ID", "Mstar"]],
    on="NGC_ID",
    how="inner"
)

data = data.dropna(subset=["Age", "FeH", "Mstar"])

# Plot Fe/H vs Age, coloured by stellar mass
fig, ax = plt.subplots(figsize=(8, 5))

sc = ax.scatter(
    data["FeH"],
    data["Age"],
    c=data["Mstar"],
    s=40,
    alpha=0.8
)

ax.set_xlabel("[Fe/H]")
ax.set_ylabel("Age (Gyr)")
ax.set_title("Age–Metallicity Relation of Globular Clusters")
ax.grid(alpha=0.25)

cbar = plt.colorbar(sc, ax=ax)
cbar.set_label(r"$M_\star$")

ax.set_xlim(data1["FeH"].min(), data1["FeH"].max())
ax.set_ylim(data1["Age"].min(), data1["Age"].max())

# Line of best fit
m, b = np.polyfit(data["FeH"], data["Age"], 1)

x_fit = np.linspace(
    data["FeH"].min(),
    data["FeH"].max(),
    100
)

y_fit = m * x_fit + b

ax.plot(x_fit, y_fit, label="Linear fit")
ax.legend()

print("Slope =", m)
print("Intercept =", b)
print("Number of matched clusters =", len(data))

plt.tight_layout()
plt.show()