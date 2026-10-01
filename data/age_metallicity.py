import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = pd.read_csv("data/vandenBerg_table2.csv")

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
print("Slope =", m)
print("Intercept =", b)

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

#table of residuals
data["Predicted_Age"] = predicted_age          #storing predicted ages and residuals to data
data["Residual"] = residual
data["z_residual"] = data["Residual"] / data["Age_err"]     #standardized residuals
data["abs_z"] = data["z_residual"].abs()                #absolute value of standardized residuals
outliers = data[
    ["#NGC", "Name", "FeH", "Age", "Age_err", "Predicted_Age", "Residual", "z_residual", "abs_z"]
]                                                           #variables of outliers table
outliers = outliers.sort_values("abs_z", ascending=False)   #sorting data by decending order of absolute standardized residuals
print(outliers.head(10))                                    #showing the 10 largest outliers in the data

plt.show()