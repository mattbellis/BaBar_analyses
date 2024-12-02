region_definitions = {}
region_definitions['Area'] = ['Fitting area', 'Signal area']
# Low and then high
region_definitions['signal MES'] = [5.27, 5.3]
region_definitions['fitting MES'] = [5.2, 5.3]

region_definitions['signal DeltaE'] = [-0.07, 0.07]
region_definitions['fitting DeltaE'] = [-0.2, 0.2]

region_definitions['sideband 1 DeltaE'] = [0.07, 0.14]
region_definitions['sideband 2 DeltaE'] = [-0.07, -0.14]
region_definitions['sideband MES'] = [5.27, 5.3]

# For the Lambda0 identification
# Define the mass cuts around the lambda
lammass_world_average = 1.115683
width = 0.003 # GeV/c^2

lo = lammass_world_average - width
hi = lammass_world_average + width

region_definitions['Lambda0 mass'] = [lo, hi]
# Which variable is this for?
region_definitions['Lambda0 flightlen'] = 1.25


