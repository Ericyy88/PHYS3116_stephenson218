import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data1 = pd.read_csv("data/HarrisPartIII.csv")
data2 = pd.read_csv("data/Krause21.csv")

# Standardise cluster identifiers
def clean_id(series):
    return (
        series.astype(str)
        .str.upper()
        .str.strip()
        .str.replace(r"[^A-Z0-9]", "", regex=True)
        .str.replace(r"^NGC0+(\d+)$", r"NGC\1", regex=True)
    )

data1["ID"] = clean_id(data1["ID"])
data2["ID"] = clean_id(data2["Object"])

# Check matching IDs
print("Common IDs:",
      len(set(data1["ID"]) & set(data2["ID"])))

# Merge
data = pd.merge(
    data2[["ID", "Mstar", "FeH"]],
    data1[["ID", "sig_v"]],
    on="ID",
    how="inner"
)

# Plot
fig, ax = plt.subplots(figsize=(8, 5))

sc = ax.scatter(
    data["Mstar"],
    data["sig_v"]**2,
    c=data["FeH"],
    cmap="coolwarm",
    s=30,
    alpha=0.8
)

ax.set_xlabel("Stellar Mass (Solar Masses)")
ax.set_ylabel(r"$\sigma_v^2$ (km$^2$/s$^2$)")
ax.set_title("Velocity Dispersion Squared vs Stellar Mass")
ax.grid(alpha=0.25)

cbar = plt.colorbar(sc, ax=ax)
cbar.set_label("[Fe/H]")

# Define x and y
x = data["Mstar"]
y = data["sig_v"]**2

# Linear regression
m, b = np.polyfit(x, y, 1)

data["predicted"] = m*x + b
data["residual"] = y - data["predicted"]

# Calculate absolute residuals
data["abs_residual"] = np.abs(data["residual"])

# Select 5 clusters with largest residuals
outliers = data.nlargest(5, "abs_residual").copy()

print("\nTop 5 outlier candidates:")
print(
    outliers[
        ["ID", "Mstar", "sig_v", "FeH", "residual"]
    ].to_string(index=False)
)

# Save to CSV
outliers.to_csv(
    "data/velocity_dispersion_outliers.csv",
    index=False
)



plt.tight_layout()
plt.show()