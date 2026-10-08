import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data1 = pd.read_csv("data/HarrisPartIII.csv")
data2 = pd.read_csv("data/Krause21.csv")

# Standardise cluster identifiers
data2["ID"] = data2["Object"].astype(str).str.strip()
data1["ID"] = data1["ID"].astype(str).str.strip()

# Merge datasets
data = pd.merge(
    data2[["ID", "Mstar", "FeH"]],
    data1[["ID", "sig_v"]],
    on="ID",
    how="inner"
)

for col in ["Mstar", "sig_v", "FeH"]:
    print(f"\n{col}:")
    print(data[col].head(15).tolist())
    print("Type:", data[col].dtype)
