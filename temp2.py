# open file sphere_au_abs_1.csv and change the second column to its negative

import pandas as pd

# Read the data
data_fdtd = pd.read_csv('data/cylinder/cylinder_au_sca_0.015.csv')

# Plot the data
import matplotlib.pyplot as plt

plt.plot(data_fdtd['Wavelength'], data_fdtd['Scattering Efficiency'], label='FDTD')
# plt.plot(data_mie['Wavelength'], data_mie['Absorption Efficiency'], label='Mie')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Scattering Efficiency')

plt.legend()
plt.show()