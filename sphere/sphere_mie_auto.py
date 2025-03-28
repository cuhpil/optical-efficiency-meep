# Plot the scattering, absorption and extinction efficiency of a gold sphere

import PyMieScatt as ps
from meep.materials import Au
import cmath
import matplotlib.pyplot as plt
import numpy as np
import argparse
import pandas as pd

# radius = [0.1, 0.3, 1, 3]
radius = [0.01]

for type in ['sca', 'abs', 'ext']:
    full_form = {'sca': 'Scattering Efficiency', 'abs': 'Absorption Efficiency', 'ext': 'Extinction Efficiency'}
    for r in radius:
        # Check if the data already exists
        try:
            data = pd.read_csv(f'data/sphere_mie/sphere_au_mie_{type}_{r}.csv')
            print(f"Data for radius {r} already exists")
        except:
            freqs = np.arange(0.2, 4, 0.1)
            eff_theory = [ps.MieQ(cmath.sqrt(Au.epsilon(f)[0, 0]),1000/f,2*r*1000,asDict=True)[f'Q{type}'] for f in freqs]

            wavelengths = 1/freqs

            # Store data in a file
            data = pd.DataFrame({'Wavelength': wavelengths, full_form[type]: eff_theory})
            data.to_csv(f'data/sphere_mie/sphere_au_mie_{type}_{r}.csv', index=False)
            print(f"Data for radius {r} created")
    
    plt.figure(dpi=150)
    for r in radius:
        data = pd.read_csv(f'data/sphere_mie/sphere_au_mie_{type}_{r}.csv')
        plt.plot(data['Wavelength'], data[full_form[type]], label=f'Radius {r} um')
    plt.grid(True,which="both",ls="-")
    plt.legend()
    plt.xlabel('Wavelength (um)')
    plt.ylabel(full_form[type])
    plt.title(f'{full_form[type]} of a Gold Sphere')
    plt.savefig(f"plots/sphere_mie/sphere_au_{type}_mie.png")
    plt.show()
if False:
    # Do the same for absorption and extinction efficiency
    try:
        data = pd.read_csv(f'data/sphere_mie/sphere_au_mie_abs_{r}.csv')
        print(f"Data for radius {r} already exists")
    except:
        freqs = np.arange(1.25, 2.5, 0.1)
        abs_eff_theory = [ps.MieQ(cmath.sqrt(Au.epsilon(f)[0, 0]),1000/f,2*r*1000,asDict=True)['Qabs'] for f in freqs]

        wavelengths = 1/freqs

        # Store data in a file
        data = pd.DataFrame({'Wavelength': wavelengths, 'Absorption Efficiency': abs_eff_theory})
        data.to_csv(f'data/sphere_mie/sphere_au_mie_abs_{r}.csv', index=False)
        print(f"Data for radius {r} created")
    
    try:
        data = pd.read_csv(f'data/sphere_mie/sphere_au_mie_ext_{r}.csv')
        print(f"Data for radius {r} already exists")
    except:
        freqs = np.arange(1.25, 2.5, 0.1)
        ext_eff_theory = [ps.MieQ(cmath.sqrt(Au.epsilon(f)[0, 0]),1000/f,2*r*1000,asDict=True)['Qext'] for f in freqs]

        wavelengths = 1/freqs

        # Store data in a file
        data = pd.DataFrame({'Wavelength': wavelengths, 'Extinction Efficiency': ext_eff_theory})
        data.to_csv(f'data/sphere_mie/sphere_au_mie_ext_{r}.csv', index=False)
        print(f"Data for radius {r} created")

    # Plot the data


    # Plot the absorption efficiency
    plt.figure(dpi=150)
    for r in radius:
        data = pd.read_csv(f'data/sphere_mie/sphere_au_mie_abs_{r}.csv')
        plt.plot(data['Wavelength'], data['Absorption Efficiency'], label=f'Radius {r} um')
    plt.grid(True,which="both",ls="-")
    plt.legend()
    plt.xlabel('Wavelength (um)')
    plt.ylabel('Absorption Efficiency')
    plt.title('Absorption Efficiency of a Gold Sphere')
    plt.savefig("sphere_au_abs_mie.png")
    plt.show()

    # Plot the extinction efficiency
    plt.figure(dpi=150)
    for r in radius:
        data = pd.read_csv(f'data/sphere_mie/sphere_au_mie_ext_{r}.csv')
        plt.plot(data['Wavelength'], data['Extinction Efficiency'], label=f'Radius {r} um')
    plt.grid(True,which="both",ls="-")
    plt.legend()
    plt.xlabel('Wavelength (um)')
    plt.ylabel('Extinction Efficiency')
    plt.title('Extinction Efficiency of a Gold Sphere')
    plt.savefig("sphere_au_ext_mie.png")
    plt.show()

