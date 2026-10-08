from pathlib import Path
import pandas as pd

# Load the table from the same folder as this script
path = Path(__file__).with_name("HarrisPartIII (2).csv")
data = pd.read_csv(path)

# Select radial velocities and remove missing values
velocities = pd.to_numeric(data["v_r"], errors="coerce").dropna()

# Calculate the sample standard deviation
sigma_v = velocities.std(ddof=1)

print(f"Number of clusters: {len(velocities)}")
print(f"Velocity dispersion: {sigma_v:.2f} km/s")
