# Get files sphere_au_abs1.csv from data/sphere and sphere_au_mie_abs_1.csv from data/sphere_mie and plot them

import pandas as pd

# Read the data
data_fdtd = pd.read_csv('data/sphere/temp_sphere_au_abs_0.03.csv')
data_mie = pd.read_csv('data/sphere_mie/sphere_au_mie_abs_0.03.csv')

# Plot the data
import matplotlib.pyplot as plt

plt.plot(data_fdtd['Wavelength'], -data_fdtd['Absorption Efficiency'], label='FDTD')
plt.plot(data_mie['Wavelength'], data_mie['Absorption Efficiency'], label='Mie')
plt.xlabel('Wavelength (nm)')
plt.ylabel('Absorption Efficiency')

plt.legend()
plt.show()