import numpy as np
from .src import theromodynamical
from .src import nozzle

thermo = thermodynamical.ThermoDynamical()
nozzle = nozzle.Nozzle()

parameters = {
    'v_dot': 0
}

if __name__ == "__main__":
    print("Hi!")