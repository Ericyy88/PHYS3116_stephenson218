from pathlib import Path
import pandas as pd

folder = Path(__file__).resolve().parent

# Read original published orbital catalogue
data = pd.read_fwf(
    folder / "tablec1.dat",
    colspecs=[
        (0, 12),    # Cluster ID
        (85, 95),   # Total orbital energy
        (96, 108)   # Angular momentum Lz
    ],
    names=["ID", "E_km2_s2", "Lz_kpc_km_s"],
    header=None
)

# Clean identifiers
data["ID"] = data["ID"].str.strip()

# Convert orbital quantities to numbers
data["E_km2_s2"] = pd.to_numeric(
    data["E_km2_s2"], errors="coerce"
)

data["Lz_kpc_km_s"] = pd.to_numeric(
    data["Lz_kpc_km_s"], errors="coerce"
)

# Remove invalid rows
data = data.dropna(
    subset=["ID", "E_km2_s2", "Lz_kpc_km_s"]
)

# Save CSV
output = folder / "orbital_energy_angular_momentum.csv"

data.to_csv(output, index=False)

print(f"Saved {len(data)} clusters to {output}")
print(data.head())