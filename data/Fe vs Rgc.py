import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data1 = pd.read_csv("data/vandenBerg_table2.csv")
data2 = pd.read_csv("data/HarrisPartI.csv")

print("Part I:")
print(data1.columns)
print("Part II:")
print(data2.columns)
