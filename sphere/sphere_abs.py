import meep as mp
import numpy as np
import matplotlib.pyplot as plt
import PyMieScatt as ps
import argparse
import cmath
from meep import materials
import pandas as pd

# Currently supports only gold and silver as materials,
# it might be made more general but that will make it more complex
parser = argparse.ArgumentParser(description="For Sphere")
parser.add_argument("-m", "--material", type=str, default="Au")
parser.add_argument("-r", "--radius", type=float, default=1)
parser.add_argument("--wmin", type = float)

args = parser.parse_args()

r = args.radius  # radius of sphere
h = 2*r  # height of sphere

# Making wavelength depend on radius fucks things up
# wvl_min = 2*np.pi/10
wvl_min = 0.4
wvl_max = 2*np.pi/2

frq_min = 1/wvl_max
frq_max = 1/wvl_min
frq_cen = 0.5*(frq_min+frq_max)
dfrq = frq_max-frq_min
nfrq = 100

## at least 8 pixels per smallest wavelength, i.e. np.floor(8/wvl_min)
resolution = 50

dpml = 0.5*wvl_max
dair = 1.0*wvl_max

pml_layers = [mp.PML(thickness=dpml)]

sr = r+dair+dpml
sz = dpml+dair+h+dair+dpml
cell_size = mp.Vector3(sr,0,sz)

sources = [mp.Source(mp.GaussianSource(frq_cen,fwidth=dfrq,is_integrated=True),
                     component=mp.Er,
                     center=mp.Vector3(0.5*sr,0,-0.5*sz+dpml),
                     size=mp.Vector3(sr)),
           mp.Source(mp.GaussianSource(frq_cen,fwidth=dfrq,is_integrated=True),
                     component=mp.Ep,
                     center=mp.Vector3(0.5*sr,0,-0.5*sz+dpml),
                     size=mp.Vector3(sr),
                     amplitude=-1j)]

sim = mp.Simulation(cell_size=cell_size,
                    boundary_layers=pml_layers,
                    resolution=resolution,
                    sources=sources,
                    dimensions=mp.CYLINDRICAL,
                    m=-1)

box_z1 = sim.add_flux(frq_cen, dfrq, nfrq, mp.FluxRegion(center=mp.Vector3(0.5*r,0,-0.5*h),size=mp.Vector3(r)))
box_z2 = sim.add_flux(frq_cen, dfrq, nfrq, mp.FluxRegion(center=mp.Vector3(0.5*r,0,+0.5*h),size=mp.Vector3(r)))
box_r = sim.add_flux(frq_cen, dfrq, nfrq, mp.FluxRegion(center=mp.Vector3(r),size=mp.Vector3(z=h)))

sim.run(until_after_sources=10)

freqs = mp.get_flux_freqs(box_z1)
box_z1_data = sim.get_flux_data(box_z1)
box_z2_data = sim.get_flux_data(box_z2)
box_r_data = sim.get_flux_data(box_r)

box_z1_flux0 = mp.get_fluxes(box_z1)

sim.reset_meep()

if args.material == "Au":
    material = materials.Au
elif args.material == "Ag":
    material = materials.Ag

geometry = [mp.Sphere(material=material,
                      center=mp.Vector3(),
                      radius=r)]

sim = mp.Simulation(cell_size=cell_size,
                    geometry=geometry,
                    boundary_layers=pml_layers,
                    resolution=resolution,
                    sources=sources,
                    dimensions=mp.CYLINDRICAL,
                    m=-1)

box_z1 = sim.add_flux(frq_cen, dfrq, nfrq, mp.FluxRegion(center=mp.Vector3(0.5*r,0,-0.5*h),size=mp.Vector3(r)))
box_z2 = sim.add_flux(frq_cen, dfrq, nfrq, mp.FluxRegion(center=mp.Vector3(0.5*r,0,+0.5*h),size=mp.Vector3(r)))
box_r  = sim.add_flux(frq_cen, dfrq, nfrq, mp.FluxRegion(center=mp.Vector3(r),size=mp.Vector3(z=h)))

sim.run(until_after_sources=100)

box_z1_flux = mp.get_fluxes(box_z1)
box_z2_flux = mp.get_fluxes(box_z2)
box_r_flux = mp.get_fluxes(box_r)

abs_flux = np.asarray(box_z1_flux)-np.asarray(box_z2_flux)-np.asarray(box_r_flux)
intensity = np.asarray(box_z1_flux0)/(np.pi*r**2)
abs_cross_section = np.divide(abs_flux,intensity)
abs_eff = -abs_cross_section/(np.pi*r**2)

abs_eff_theory = [ps.MieQ(cmath.sqrt(material.epsilon(f)[0, 0]),1000/f,2*r*1000,asDict=True)['Qabs'] for f in freqs]
abs_cross_section_theory = np.array(abs_eff_theory)*np.pi*r**2

freqs = np.array(freqs)
abs_eff = np.array(abs_eff)
# Store data in a file in the folder data_fdtd

data = pd.DataFrame({'Wavelength': 1/freqs, 'Absorption Efficiency': abs_eff})
data.to_csv(f'data/sphere/sphere_{args.material.lower()}_abs_{r}.csv', index=False)


if mp.am_master():
    plt.figure(dpi=150)
    plt.loglog(2*np.pi*r*np.asarray(freqs),abs_cross_section,'bo-')
    # plt.loglog(2*np.pi*r*np.asarray(freqs),abs_cross_section_theory,'ro-')
    plt.grid(True,which="both",ls="-")
    plt.xlabel('(sphere circumference)/wavelength, 2πr/λ')
    plt.ylabel('Absorption cross section, σ')
    plt.title(f'Absprption Cross Section of a {args.material} Sphere of radius {r} um')
    plt.tight_layout()
    plt.savefig(f"plots/sphere/sphere_abs_{args.material}_{r}.png")