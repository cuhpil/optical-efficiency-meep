import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Define the folder path
base_path = "data/cylinder"

# Extract available radius values from filenames
radii = [0.015, 0.03, 0.045]

# Define a color map for each radius
color_map = {0.015: "blue", 0.03: "green", 0.045: "red"}

# Initialize plot
plt.figure(figsize=(8, 6))

# Loop over each radius
for radius in radii:
    abs_file = os.path.join(base_path, f"cylinder_au_abs_{radius}.csv")
    sca_file = os.path.join(base_path, f"cylinder_au_sca_{radius}.csv")

    # Load data
    if os.path.exists(abs_file) and os.path.exists(sca_file):
        abs_data = pd.read_csv(abs_file)
        sca_data = pd.read_csv(sca_file)

        # Assuming first column is wavelength and second column is efficiency
        wavelength = abs_data.iloc[:, 0]
        abs_eff = abs(abs_data.iloc[:, 1])
        sca_eff = abs(sca_data.iloc[:, 1])
        ext_eff = abs_eff + sca_eff  # Compute extinction efficiency

        # Plot data with consistent colors
        plt.plot(wavelength, abs_eff, linestyle="dashed", color=color_map[radius], label=f"Abs {radius} μm", alpha=0.8)
        plt.plot(wavelength, sca_eff, linestyle="dotted", color=color_map[radius], label=f"Sca {radius} μm", alpha=0.8)
        plt.plot(wavelength, ext_eff, linestyle="solid", color=color_map[radius], label=f"Ext {radius} μm", alpha=0.8)

    else:
        print(f"Missing data for radius {radius}. Skipping...")

# Formatting the plot
plt.xlabel("Wavelength (nm)")
plt.ylabel("Efficiency")
plt.title("Optical Efficiencies for Cylinders of Different Radii\n Ratio of length of cylinder to its radius is 4")
plt.legend()
plt.grid(True)
plt.savefig("plots/cylinder_efficiencies.png", dpi=300)

# Show the plot
plt.show()
