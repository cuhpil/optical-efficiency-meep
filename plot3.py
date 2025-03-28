import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Define the folder path
base_path = "data/cylinder"
plot_path = "plots"
os.makedirs(plot_path, exist_ok=True)  # Ensure plot directory exists

# Defined radii values
radii = [0.015, 0.03, 0.045]

# Create separate figures for each efficiency type
fig_abs, ax_abs = plt.subplots(figsize=(8, 6))
fig_sca, ax_sca = plt.subplots(figsize=(8, 6))
fig_ext, ax_ext = plt.subplots(figsize=(8, 6))

# Loop over each radius
for radius in radii:
    abs_file = os.path.join(base_path, f"cylinder_au_abs_{radius}.csv")
    sca_file = os.path.join(base_path, f"cylinder_au_sca_{radius}.csv")

    # Load data if both files exist
    if os.path.exists(abs_file) and os.path.exists(sca_file):
        abs_data = pd.read_csv(abs_file)
        sca_data = pd.read_csv(sca_file)

        # Assuming first column is wavelength and second column is efficiency
        wavelength = abs_data.iloc[:, 0]
        abs_eff = abs(abs_data.iloc[:, 1])
        sca_eff = abs(sca_data.iloc[:, 1])
        ext_eff = abs_eff + sca_eff  # Compute extinction efficiency

        # Plot absorption efficiency
        ax_abs.plot(wavelength, abs_eff, linestyle="solid", label=f"Abs {radius} μm", alpha=0.8)

        # Plot scattering efficiency
        ax_sca.plot(wavelength, sca_eff, linestyle="solid", label=f"Sca {radius} μm", alpha=0.8)

        # Plot extinction efficiency
        ax_ext.plot(wavelength, ext_eff, linestyle="solid", label=f"Ext {radius} μm", alpha=0.8)

    else:
        print(f"Missing data for radius {radius}. Skipping...")

# Format the plots
for ax, title, filename in zip(
    [ax_abs, ax_sca, ax_ext],
    ["Absorption Efficiency", "Scattering Efficiency", "Extinction Efficiency"],
    ["absorption.png", "scattering.png", "extinction.png"]
):
    ax.set_xlabel("Wavelength (nm)")
    ax.set_ylabel("Efficiency")
    ax.set_title(title)
    ax.legend()
    ax.grid(True)
    fig = ax.get_figure()
    fig.savefig(os.path.join(plot_path, filename), dpi=300)

# Show all plots
plt.show()
