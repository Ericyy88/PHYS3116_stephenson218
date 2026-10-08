import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


outlier_clusters = pd.read_csv("data/outlier_clusters.csv")
Position = pd.read_csv("data/outer_gcs.csv")

# Convert NGC number to strings such as "NGC 104"
outlier_clusters["ID"] = outlier_clusters["#NGC"].apply(
    lambda x: f"NGC {int(x)}" if str(x).replace(".", "", 1).isdigit()
    else str(x)
)

print("Outlier clusters:", outlier_clusters["ID"].tolist())
print("Outer clusters:", Position["ID"].tolist())