"""
nozzle.py
"""
import numpy as np
from . import theromochemical

class Nozzle(object):
    g0 = 9.8
    
    def evaluation(n, input):
        mdot = input['mdot']
        OF = input['OF']
        p1 = input['p1']
        p2 = input['p3']
        At = input['At']
        k = input['k']
        T0 = input['T0']
        v2 = np.sqrt(2*k)
        F = mdot * v2
        isp = F / (mdot * n.g0)
        
        return F, v2, isp, mdot