import json
from .trajectory import config

class Parameters:
    def __init__(self):
        self.package = []
        
        file = open(path, 'r')
        extension = path.split(".")[1]
    
        if extension == "params":
            subgroup = []
            
            for line in file.readlines():
                if line[0] == '=':
                    self.package.append(subgroup[:])

                else:
                    x = line.split(':')
                    subgroup.append(self.cast(x[1].strip()))
                
    def cast(self, x):
        try:
            return float(x)
        except Exception as err:
            if config.developer != False:
                print("Received error: {}".format(err))
            else:
                return str(x)