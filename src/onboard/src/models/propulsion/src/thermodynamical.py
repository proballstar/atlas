"""
thermodynamical.py
"""
import numpy as np
from . import theromochemical

class ThermoDynamical(object):
    def __init__(t):
        # Constants
        t.C0 = 0.047
        
        t.hv = 2.3 # Vaporization heat
    
    def evaluation(t, input):
        thermo = {}
        
        return thermo