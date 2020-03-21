"""
thermochemical.py
"""
import numpy as np
import matplotlib.pyplot as plt

# Pressure Average = 5%
# Permissible Loss = 5%
of = np.arange(1, 12.5, 0.5)

# Heat Ratio
k = np.array([
    1.22
])

# Molecular weight in kilograms
m = np.array([
    22,
    22
])

# Combustion 
cs = np.array([
    1250,
    1325
])

# Flame temperature
T0 = np.array([
    1800,
    2000
])

# Viscosity
viscosity = np.array([
    .55,
    .60
])

# Prandtl number
Pr = np.array([
    .50,
    .51
])

plt.plot(of, Pr)