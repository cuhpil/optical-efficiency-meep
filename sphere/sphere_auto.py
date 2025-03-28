# Write a script to run the file sphere.py for different radius and material arguments

# Run the sphere file for range of radii 0.1, 0.3 and 1 and materials Au and Ag

import os

materials = ['Au']
radii = [0.01, 0.03, 0.1, 0.3, 1.0, 3.0]

for type in ['sca', 'abs']:
    full_form = {'sca': 'Scattering Efficiency', 'abs': 'Absorption Efficiency'}
    for material in materials:
        for radius in radii:
            # Check if the file already exists, the file name is of form sphere_au_{type}_{radius}.csv
            file_name = f'data/sphere/sphere_{material.lower()}_{type}_{radius}.csv'
            if os.path.exists(file_name):
                print(f"File {file_name} already exists")
                continue

            # Run the sphere_{type}.py file
            os.system(f'mpirun -np 5 python3 sphere/sphere_{type}.py --material {material} --radius {radius}')
            # Check if the file was created
            if os.path.exists(file_name):
                print(f"File {file_name} created")
            else:
                raise Exception(f"File {file_name} not created")


        

