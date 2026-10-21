import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data1 = pd.read_csv("data/HarrisPartIII_standardized.csv")
data2 = pd.read_csv("data/Krause21_standardized.csv")

data = pd.merge(
    data1[["ID", "sig_v", "sig_v_e"]],
    data2[["ID", "Mstar", "FeH"]],
    on="ID",
    how="inner"
)                      

data = data.dropna(subset=["Mstar", "sig_v"])

data["sig_v2"] = data["sig_v"] ** 2

data["log_M"] = np.log10(data["Mstar"])
data["log_sig_v2"] = np.log10(data["sig_v2"])


m, b = np.polyfit(data["log_M"], data["log_sig_v2"], 1)
data["predicted"] = m * data["log_M"] + b
data["residual"] = data["log_sig_v2"] - data["predicted"]
std = data["residual"].std(ddof=1)


#residual plot
predicted_mass = m * data["log_M"] + b                   #predicted ages based on the linear fit
residual = data["log_sig_v2"] - predicted_mass                #calculating residuals
fig2, ax2 = plt.subplots(figsize=(8, 5))    
ax2.errorbar(data["log_M"], residual, fmt="o", markersize=4, capsize=3, color="navy", ecolor="lightgray", elinewidth=1)
ax2.set_xlabel(r"$\log_{10}(M_\star/M_\odot)$")
ax2.set_ylabel(r"$\log_{10}(\sigma_v^2/(\mathrm{km/s})^2)$ - Predicted")
ax2.set_title("Residuals of Velocity Dispersion vs Stellar Mass")
ax2.grid(alpha=0.25)
ax2.axhline(0)


# Standardise residuals using their standard deviation
data["z_residual"] = data["residual"] / std
data["abs_z"] = data["z_residual"].abs()

# Rank all clusters by residual magnitude
ranked = data.sort_values("abs_z", ascending=False)

# Select top 20 clusters with largest absolute residuals
sig_v_outliers = ranked.head(20).copy()

print("\nTop 20 outliers:")
print(sig_v_outliers[
    ["ID", "FeH", "Mstar", "sig_v2", "residual", "abs_z"]
])

sig_v_outliers[["ID"]].to_csv(
    "Sig_v_outliers.csv", index=False
)



fig, ax = plt.subplots(figsize=(8, 5))

# Scatter plot
ax.scatter(
    data["log_M"],
    data["log_sig_v2"],
    color="navy",
    s=20,
    alpha=0.7
)

# Regression line
x_fit = np.linspace(data["log_M"].min(), data["log_M"].max(), 200)
y_fit = m * x_fit + b

ax.plot(
    x_fit,
    y_fit,
    color="navy",
    linewidth=2,
    label=f"Linear fit: y = {m:.3f}x + {b:.3f}"
)

ax.set_xlabel(r"$\log_{10}(M_\star/M_\odot)$")
ax.set_ylabel(r"$\log_{10}(\sigma_v^2/(\mathrm{km/s})^2)$")
ax.set_title("Velocity Dispersion vs Stellar Mass of Clusters")

ax.grid(alpha=0.25)
ax.legend()

plt.show()


