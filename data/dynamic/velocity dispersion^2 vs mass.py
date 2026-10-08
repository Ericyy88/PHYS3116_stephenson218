"""Plot central velocity dispersion squared against globular-cluster mass.

Put Krause21.csv and HarrisPartIII (2).csv beside this script, then run it.
Requires pandas, numpy and matplotlib. Optional command-line arguments allow
other input paths and an output folder; --no-show saves without opening a window.

Mass units are 10^5 solar masses, verified against Table B.1 of Krause et al.
(2016), A&A 587, A53: https://doi.org/10.1051/0004-6361/201526685.
The supplied mass file is named Krause21.csv. Its original values are retained.
Harris sig_v is the central internal velocity dispersion, in km/s.
"""

from pathlib import Path
import argparse

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def normalise_names(names):
    """Match catalogue IDs, including two alternate spellings."""
    return (
        names.astype("string")
        .str.upper()
        .str.replace(r"\s+", "", regex=True)
        .replace({"RUPRECHT106": "RUP106", "PALOMAR12": "PAL12"})
    )


def main():
    script_folder = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mass-file", type=Path,
                        default=script_folder / "Krause21.csv")
    parser.add_argument("--dispersion-file", type=Path,
                        default=script_folder / "HarrisPartIII (2).csv")
    parser.add_argument("--output-dir", type=Path, default=script_folder)
    parser.add_argument("--no-show", action="store_true")
    args = parser.parse_args()

    masses = pd.read_csv(args.mass_file)
    harris = pd.read_csv(args.dispersion_file)
    masses = masses.loc[masses["Class"].eq("GC")].copy()

    # Join by cluster identity, never by row number.
    masses["cluster_key"] = normalise_names(masses["Object"])
    harris["cluster_key"] = normalise_names(harris["ID"])
    joined = masses.merge(
        harris[["cluster_key", "ID", "sig_v", "sig_v_e"]],
        on="cluster_key", how="left", validate="one_to_one", indicator=True
    )

    for column in ["Mstar", "sig_v", "sig_v_e"]:
        joined[column] = pd.to_numeric(joined[column], errors="coerce")

    # Missing velocities are unavailable, not zero. Keep every valid pair.
    valid = (
        np.isfinite(joined["Mstar"]) & np.isfinite(joined["sig_v"])
        & (joined["Mstar"] > 0) & (joined["sig_v"] > 0)
    )
    data = joined.loc[valid].sort_values("Mstar").copy()
    if data.empty:
        raise ValueError("No clusters have both a valid mass and dispersion.")

    # Mstar stays in units of 10^5 solar masses for the plotted x axis.
    data["mass_msun"] = data["Mstar"] * 100_000
    data["sigma_v_squared"] = data["sig_v"] ** 2
    # First-order uncertainty propagation for y = sigma_v^2.
    data["sigma_v_squared_error"] = 2 * data["sig_v"] * data["sig_v_e"]

    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 12,
        "axes.labelsize": 14, "axes.titlesize": 17,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.edgecolor": "#536174", "xtick.color": "#334155",
        "ytick.color": "#334155", "text.color": "#172033",
        "axes.labelcolor": "#172033", "savefig.facecolor": "white"
    })
    fig, ax = plt.subplots(figsize=(9.6, 6.5))
    fig.subplots_adjust(left=0.12, right=0.97, bottom=0.23, top=0.84)
    fig.text(0.12, 0.94, "Velocity dispersion squared vs stellar mass",
             fontsize=17, fontweight="bold", va="top")
    fig.text(0.12, 0.88,
             f"{len(data)} globular clusters with both measurements",
             fontsize=12, color="#586579", va="top")

    has_error = (
        np.isfinite(data["sigma_v_squared_error"])
        & data["sigma_v_squared_error"].ge(0)
    )
    ax.errorbar(
        data.loc[has_error, "Mstar"],
        data.loc[has_error, "sigma_v_squared"],
        yerr=data.loc[has_error, "sigma_v_squared_error"],
        fmt="none", ecolor="#9DACBC", elinewidth=1.1,
        capsize=2.5, zorder=2
    )
    ax.scatter(data["Mstar"], data["sigma_v_squared"], s=49,
               color="#23628F", edgecolor="white", linewidth=0.7, zorder=3)
    ax.set_xlabel(r"Stellar mass, $M_\star$ ($10^5\,M_\odot$)", labelpad=10)
    ax.set_ylabel(r"Central dispersion squared, $\sigma_v^2$ ($\mathrm{km^2\,s^{-2}}$)",
                  labelpad=10)
    ax.set_xlim(left=0, right=data["Mstar"].max() * 1.08)
    upper_values = data["sigma_v_squared"] + data["sigma_v_squared_error"].fillna(0)
    ax.set_ylim(bottom=0, top=upper_values.max() * 1.08)
    ax.grid(True, color="#E4E9EF", linewidth=0.7, zorder=0)
    ax.set_axisbelow(True)
    fig.text(0.12, 0.09,
             r"Vertical errors: $\Delta(\sigma_v^2)\approx2\sigma_v\Delta\sigma_v$.",
             fontsize=10, color="#586579")
    fig.text(0.12, 0.05,
             "Masses: supplied Krause table. Central dispersions: supplied Harris table.",
             fontsize=10, color="#586579")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    image_path = args.output_dir / "sigma2_vs_mass.png"
    data_path = args.output_dir / "sigma2_vs_mass_data.csv"
    fig.savefig(image_path, dpi=240)
    data[["ID", "Object", "Mstar", "mass_msun", "sig_v", "sig_v_e",
          "sigma_v_squared", "sigma_v_squared_error"]].rename(columns={
        "ID": "cluster", "Object": "mass_catalogue_id",
        "Mstar": "mass_1e5_msun", "sig_v": "sigma_v_km_s",
        "sig_v_e": "sigma_v_error_km_s",
        "sigma_v_squared": "sigma_v_squared_km2_s2",
        "sigma_v_squared_error": "sigma_v_squared_error_km2_s2"
    }).to_csv(data_path, index=False)

    print(f"Catalogue matches: {joined['_merge'].eq('both').sum()} of {len(masses)}")
    print(f"Plotted clusters: {len(data)}")
    print(f"Excluded without a valid mass or dispersion: {len(joined) - len(data)}")
    print(f"Saved plot: {image_path}")
    print(f"Saved plotted data: {data_path}")
    if not args.no_show:
        plt.show()
    plt.close(fig)


if __name__ == "__main__":
    main()
