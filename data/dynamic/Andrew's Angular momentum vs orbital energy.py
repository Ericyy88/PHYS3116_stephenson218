"""Plot published orbital energy against angular momentum for Harris clusters.

Save orbital_energy_angular_momentum.csv beside this Python file, then run it.
Requires pandas and matplotlib.

Orbital source: De Leo et al. (2026), A&A 706, A130, Table C.1.
Paper DOI: https://doi.org/10.1051/0004-6361/202556235
Catalogue: https://cdsarc.cds.unistra.fr/ftp/J/A+A/706/A130/tablec1.dat
Column definitions: https://cdsarc.cds.unistra.fr/ftp/J/A+A/706/A130/ReadMe

The accompanying CSV matches published values to the uploaded Harris Part I.
Matches use cluster IDs, equivalent Ter/Terzan and Djor/Djorg spellings, and
Harris alternate names. The orbital_ID column preserves the source identifier.
152 of 157 Harris clusters match; Ko 1, Ko 2, BH 176, GLIMPSE01 and GLIMPSE02
have no matching entry and are excluded.

E is specific orbital energy in km^2/s^2, and Lz is specific angular momentum
in kpc km/s. This catalogue defines negative Lz as prograde and positive Lz
as retrograde. Values depend on the Galactic potential adopted by the authors.
The rotating bar means E and Lz need not be constant along an orbit.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


folder = Path(__file__).resolve().parent
data = pd.read_csv(folder / "orbital_energy_angular_momentum.csv")

# Scale the axes to keep their tick labels easy to read.
angular_momentum = data["Lz_kpc_km_s"] / 1000
orbital_energy = data["E_km2_s2"] / 100000

fig, ax = plt.subplots(figsize=(10, 6.5))
ax.scatter(
    angular_momentum, orbital_energy,
    s=35, color="#286da8", alpha=0.80, edgecolors="white", linewidths=0.5,
)
ax.axvline(0, color="#727c87", linestyle="--", linewidth=1)
ax.set_axisbelow(True)
ax.grid(alpha=0.20)

ax.set_xlabel(r"Specific angular momentum $L_z$ [$10^3$ kpc km s$^{-1}$]", fontsize=12)
ax.set_ylabel(r"Specific orbital energy $E$ [$10^5$ km$^2$ s$^{-2}$]", fontsize=12)
ax.set_xlim(-3.7, 3.5)
ax.set_ylim(-2.85, -0.08)
ax.tick_params(labelsize=11)
ax.spines[["top", "right"]].set_visible(False)

ax.text(0.24, 1.02, "Prograde (same direction as the disc)",
        transform=ax.transAxes, ha="center", va="bottom", fontsize=10, color="#475569")
ax.text(0.76, 1.02, "Retrograde (opposite direction)",
        transform=ax.transAxes, ha="center", va="bottom", fontsize=10, color="#475569")

# Label a few reference clusters. These labels are not an outlier classification.
label_offsets = {
    "NGC 104": (-14, -18),
    "NGC 2419": (15, 18),
    "NGC 3201": (-12, -20),
    "NGC 5139": (15, -18),
    "NGC 6101": (-12, 16),
    "Pal 1": (12, -18),
    "Pal 12": (-12, -22),
}
for cluster_id, offset in label_offsets.items():
    row = data.loc[data["ID"] == cluster_id].iloc[0]
    ax.annotate(
        cluster_id,
        xy=(row["Lz_kpc_km_s"] / 1000, row["E_km2_s2"] / 100000),
        xytext=offset, textcoords="offset points",
        ha="right" if offset[0] < 0 else "left", fontsize=9, color="#1e293b",
        arrowprops={"arrowstyle": "-", "color": "#94a3b8", "lw": 0.7},
        bbox={"boxstyle": "round,pad=0.15", "fc": "white", "ec": "none", "alpha": 0.9},
    )

fig.suptitle("Globular cluster orbital energy vs angular momentum", fontsize=16, y=0.97)
fig.text(0.5, 0.923,
         f"{len(data)} Harris clusters. Orbital values from De Leo et al. (2026).",
         ha="center", fontsize=10.5, color="#475569")
fig.text(0.5, 0.028,
         "Each point is a globular cluster. Catalogue convention: negative Lz is prograde.",
         ha="center", fontsize=9, color="#475569")
fig.subplots_adjust(left=0.12, right=0.97, bottom=0.16, top=0.86)

output = folder / "orbital_energy_vs_angular_momentum.png"
fig.savefig(output, dpi=240, facecolor="white")
print(f"Plotted {len(data)} clusters. Saved: {output}")
plt.show()
