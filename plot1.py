import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Define the radii to loop over
radii = [0.03, 0.1, 0.3, 1, 3]

# Define base paths
base_paths = {
    "FDTD": "data/sphere",
    "Mie": "data/sphere_mie"
}

# Loop over each radius
for radius in radii:
    plt.figure(figsize=(8, 6))


    for label, base_path in base_paths.items():
        # Construct file paths
        if radius < 0.2 and label == "FDTD":
            abs_file = os.path.join(base_path, f"temp_sphere_au_abs_{radius}.csv")
            sca_file = os.path.join(base_path, f"sphere_au_sca_{radius}.csv")
        elif label == "Mie":
            abs_file = os.path.join(base_path, f"sphere_au_mie_abs_{radius}.csv")
            sca_file = os.path.join(base_path, f"sphere_au_mie_sca_{radius}.csv")
            # ext_file = os.path.join(base_path, f"sphere_au_mie_ext_{radius}.csv")
        else:
            abs_file = os.path.join(base_path, f"sphere_au_abs_{float(radius)}.csv")
            sca_file = os.path.join(base_path, f"sphere_au_sca_{float(radius)}.csv")

        # Check if both files exist
        if os.path.exists(abs_file) and os.path.exists(sca_file):
            # Load data
            abs_data = abs(pd.read_csv(abs_file))
            sca_data = abs(pd.read_csv(sca_file))
            # if label == "Mie":
            #     ext_data = abs(pd.read_csv(ext_file))

            # Filter data based on wavelength range
            abs_data = abs_data[(abs_data.iloc[:, 0] >= 0.4) * (abs_data.iloc[:, 0] <= 1)]
            sca_data = sca_data[(sca_data.iloc[:, 0] >= 0.4) * (sca_data.iloc[:, 0] <= 1)]
            # if label == "Mie":
            #     ext_data = ext_data[(ext_data.iloc[:, 0] >= 0.4) * (ext_data.iloc[:, 0] <= 1)]

            # Assuming first column is wavelength and second column is efficiency
            wavelength_abs = abs_data.iloc[:, 0]
            wavelength_sca = sca_data.iloc[:, 0]
            abs_eff = abs_data.iloc[:, 1]
            sca_eff = sca_data.iloc[:, 1]
            # if label == "Mie":
            #     ext_eff = ext_data.iloc[:, 1]
            # else:
            #     ext_eff = abs_eff + sca_eff
                # This won't work correctly because abs_eff and sca_eff might not be on the same wavelength grid
                # You would need to interpolate them to a common grid first
                # Hence I'm commenting out the ext part


            # Get something like a union of the wavelengths

            # Plot data
            plt.plot(wavelength_abs*1000, abs_eff, linestyle="dashed", label=f"{label} Absorption", alpha=0.8)
            if radius > 0.03:
                plt.plot(wavelength_sca*1000, sca_eff, linestyle="solid", label=f"{label} Scattering", alpha=0.8)
            # plt.plot(wavelength, ext_eff, linestyle="solid", label=f"{label} Extinction", alpha=0.8)

        else:
            print(f"Missing data for {label}, radius {radius}. Skipping...")

    # Formatting the plot
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Efficiency")
    plt.title(f"Optical Efficiencies for Radius {radius} μm")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"plots/sphere/sphere_eff_{radius}.png")
    # Show the plot
    plt.show()
