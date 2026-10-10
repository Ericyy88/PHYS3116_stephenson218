data["age_outlier"] = data["ID"].isin(
    pd.read_csv("Age_outliers.csv")["ID"]
)

fig, ax = plt.subplots(figsize=(7, 5))

ax.boxplot(
    [
        data.loc[~data["age_outlier"], "R_gc"],
        data.loc[data["age_outlier"], "R_gc"]
    ],
    tick_labels=["Other clusters", "Age outliers"]
)

ax.set_ylabel("Galactocentric Distance (kpc)")
ax.set_title("Galactocentric Distance by Age-Metallicity Group")
ax.grid(axis="y", alpha=0.25)

plt.show()