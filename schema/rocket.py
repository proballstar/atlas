class Rocket(object):
    def __init__(self, fuel, mass, SA, nozzle, exV, exP):
        self.fuel = fuel
        self.mass = mass
        self.SA = SA
        self.nozzle = nozzle
        self.exV = exV
        self.exP = exP
        self.velocity = 0
        self.height = 0

    def calcHeight(self, t, inc):
        for x in range(inc):
            # get acc (use g0 for now)
            # no drag loss for now
            acc = (self.calcThrust(0) - self.mass*9.80665)/self.mass
            # get new mass (mass - massflow/inc)
            self.mass -= self.exV*self.nozzle*1.0/inc
            # "move" the rocket
            self.velocity += acc/inc
            self.height += self.velocity/inc
        return self.height

    def calcThrust(self, alt):
        mflow = self.exV*self.nozzle*1.0  # fuel density is 1.0 for now
        # eventually get correct pressure at altitude
        # for now use 101325
        thrust = mflow*self.exV + self.nozzle*(self.exP - 101325.0)
        return thrust


rocket1 = Rocket(75.0, 1000.0, 10.0, 1.0, 400.0, 101325.0)

print(rocket1.calcHeight(2, 120))
