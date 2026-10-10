import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv("data/vandenBerg_table2_standardized.csv")

#define x and y values
x = data["FeH"]                                     #defining x as the metallicity values from the data
y = data["Age"]                                     #defining y as the age values from the data

#Plotting age vs cluster 
fig, ax = plt.subplots(figsize=(8, 5))
#uncertainties
ax.errorbar(
    x,
    y,
    yerr=data["Age_err"],
    fmt="o",
    markersize=4,
    capsize=3,
    color="navy",
    ecolor="lightgray",
    elinewidth=1,
)

ax.set_xlabel("[Fe/H]")
ax.set_ylabel("Age (Gyr)")
ax.set_title("Age vs Metallicity of Clusters")
ax.grid(alpha = 0.25)


#line of best fit
m, b = np.polyfit(x, y, 1)                  #linear regression of degree 1
x_fit = np.linspace(x.min(), x.max(), 100) 
y_fit = m * x_fit + b                       #equation of the line        
ax.plot(x_fit, y_fit, label="Linear fit")   #plotting the line of best fit
ax.legend()

#residual plot
predicted_age = m * x + b                   #predicted ages based on the linear fit
residual = y - predicted_age                #calculating residuals
fig2, ax2 = plt.subplots(figsize=(8, 5))    
ax2.errorbar(x, residual, yerr=data["Age_err"], fmt="o", markersize=4, capsize=3, color="navy", ecolor="lightgray", elinewidth=1)
ax2.set_xlabel("[Fe/H]")
ax2.set_ylabel("Residuals")
ax2.set_title("Residuals of Age vs Metallicity")
ax2.grid(alpha=0.25)
ax2.axhline(0)

# Table of residuals
data["Predicted_Age"] = predicted_age
data["Residual"] = residual

# Standardised residuals
data["z_residual"] = data["Residual"] / data["Age_err"]
data["abs_z"] = data["z_residual"].abs()

# Rank all clusters by largest absolute standardised residual
ranked = data.sort_values("abs_z", ascending=False)

# Select top 10 outliers
age_outliers = ranked.head(20).copy()

print("\nTop 20 Age-Metallicity Outliers:")
print(age_outliers[
    ["ID", "FeH", "Age", "Predicted_Age", "Residual", "abs_z"]
].to_string(index=False))

# Save top 20 cluster IDs
age_outliers[["ID"]].to_csv(
    "Age_outliers.csv", index=False
)

plt.show()

