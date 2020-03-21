"""
injector.py
"""
import numpy as np

def evaluation(run):
    qv = run['Cd']
    qm = run['rho'] * qv
    
    return qm

injector = {
    'rho': 1000, # Water
    'D': 3.175e-3, # Pipe diameter
    'd': 1.53-3, # Hole diameter
    'dP': 172e3, # Delta pressure
    'Cd': 0.82, # Discharge coefficient
    'md': 1.3 # Kilograms per second
}