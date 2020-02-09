# The MIT License
#
# Copyright (c) 2019 - Present Firebolt, Inc. & Firebolt Space Agency(FSA).
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
from src.telemachus import get_telemetry, KSPNotConnected, check_connection
from src.maneuver import Burn
from src import utils, maneuver
import inspect
import sys
import math
from collections import OrderedDict


from PyQt5.QtCore import QTimer

from src import config
if config.DEBUG:
    from pudb import set_trace


class Program(object):

    computer = None

    def __init__(self, description, number):

        self.computer = Program.computer
        self.description = description
        self.number = number

    def execute(self):

        utils.log("Executing Program {}: {}".format(
            self.number, self.description))
        self.computer.flash_comp_acty(500)
        self.computer.dsky.set_register(self.number, "program")
        self.computer.running_program = self

    def terminate(self):

        if self.computer.running_program == self:
            self.computer.running_program = None

    def restart(self):

        self.execute()

    def __str__(self):
        return "Program {} ({}) ".format(self.number, self.description)


class Program00(Program):

    def __init__(self):

        super(Program00, self).__init__(description="AGC Idling", number="00")


class Program01(Program):

    def __init__(self):

        super().__init__(description="Prelaunch or service - Initialization program", number="01")
        self.timer = QTimer()
        self.timer.timeout.connect(self.timeout)

    def execute(self):

        super().execute()
        if check_connection() == False:
            Program.computer.poodoo_abort(111)
            self.terminate()
            return
        Program.computer.imu.on()
        self.timer.start(10000)

    def timeout(self):

        Program.computer.imu.set_fine_align()
        Program.computer.execute_program("02")


class Program02(Program):

    def __init__(self):

        super().__init__(description="Prelaunch or service - Gyrocompassing program", number="02")
        self.timer = QTimer()
        self.timer.timeout.connect(self.timeout)

    def execute(self):

        super().execute()
        Program.computer.add_to_mainloop(self.check_for_liftoff)

    def check_for_liftoff(self):
        if get_telemetry("verticalSpeed") > 1:
            utils.log("Liftoff discrete")
            Program.computer.remove_from_mainloop(self.check_for_liftoff)

            for register in ["verb", "noun", "program", "data_1", "data_2", "data_3"]:
                Program.computer.dsky.blank_register(register)
            self.timer.start(1000)

    def timeout(self):
        self.timer.stop()
        Program.computer.execute_program("11")


class Program11(Program):

    def __init__(self):

        super().__init__(description="Earth Orbit Insertion Monitor", number="11")

    def execute(self):

        super().execute()
        utils.log("Program 11 executing", log_level="INFO")

        if check_connection() == False:
            return

        if "02" in self.computer.running_programs:
            self.computer.programs["02"].terminate()

        self.computer.execute_verb(verb="16", noun="62")


class Program15(Program):

    def __init__(self):
        # V37E15E

        super().__init__(description="TMI Calculate", number="15")

    def execute(self):

        super().execute()

        if not check_connection():
            self.computer.poodoo_abort(111)
            self.terminate()
            return

        is_orbit_ok = maneuver.HohmannTransfer.check_orbital_parameters()
        if is_orbit_ok == True:
            self.computer.execute_verb(verb="21", noun="25")
            self.computer.dsky.request_data(
                requesting_object=self._accept_initial_mass_whole_part, display_location="data_1")
        else:
            self.computer.poodoo_abort(is_orbit_ok[1])

    def _accept_initial_mass_whole_part(self, mass):
        Program.computer.noun_data["25"][0] = mass
        self.computer.execute_verb(verb="22", noun="25")
        self.computer.dsky.request_data(
            requesting_object=self._accept_initial_mass_fractional_part, display_location="data_2")

    def _accept_initial_mass_fractional_part(self, mass):
        Program.computer.noun_data["25"][1] = mass
        self.computer.execute_verb(verb="21", noun="31")
        self.computer.dsky.request_data(
            requesting_object=self._accept_thrust_whole_part, display_location="data_1")

    def _accept_thrust_whole_part(self, thrust):
        Program.computer.noun_data["31"][0] = thrust
        self.computer.execute_verb(verb="22", noun="31")
        self.computer.dsky.request_data(
            requesting_object=self._accept_thrust_fractional_part, display_location="data_2")

    def _accept_thrust_fractional_part(self, thrust):
        Program.computer.noun_data["31"][1] = thrust
        self.computer.execute_verb(verb="21", noun="38")
        self.computer.dsky.request_data(
            requesting_object=self._accept_isp, display_location="data_1")

    def _accept_isp(self, isp):
        Program.computer.noun_data["38"][0] = isp
        self.calculate_maneuver()

    def calculate_maneuver(self):
        self.maneuver = maneuver.HohmannTransfer()
        self.maneuver.execute()
        self.computer.execute_verb(verb="06", noun="95")
        self.computer.go_to_poo()


class Program31(Program):

    def __init__(self):
        super().__init__(description="MOI Burn Calculator", number="31")
        self.delta_v = Program.computer.moi_burn_delta_v
        self.time_of_node = get_telemetry("timeOfPeriapsisPassage")
        self.time_of_ignition = None

    def update_parameters(self):

        self.delta_v = Program.computer.moi_burn_delta_v
        self.time_of_node = get_telemetry("timeOfPeriapsisPassage")

        initial_mass = float(
            self.computer.noun_data["25"][0] + "." + self.computer.noun_data["25"][1])
        thrust = float(
            self.computer.noun_data["31"][0] + "." + self.computer.noun_data["31"][1])
        specific_impulse = float(self.computer.noun_data["38"][0])
        self.duration_of_burn = maneuver.calc_burn_duration(
            initial_mass, thrust, specific_impulse, self.delta_v)
        self.time_of_ignition = self.time_of_node - (self.duration_of_burn / 2)

    def execute(self):

        self.computer.execute_verb(verb="21", noun="25")
        self.computer.dsky.request_data(
            requesting_object=self._accept_initial_mass_whole_part, display_location="data_1")

    def _accept_initial_mass_whole_part(self, mass):
        Program.computer.noun_data["25"][0] = mass
        self.computer.execute_verb(verb="22", noun="25")
        self.computer.dsky.request_data(
            requesting_object=self._accept_initial_mass_fractional_part, display_location="data_2")

    def _accept_initial_mass_fractional_part(self, mass):
        Program.computer.noun_data["25"][1] = mass
        self.computer.execute_verb(verb="21", noun="31")
        self.computer.dsky.request_data(
            requesting_object=self._accept_thrust_whole_part, display_location="data_1")

    def _accept_thrust_whole_part(self, thrust):
        Program.computer.noun_data["31"][0] = thrust
        self.computer.execute_verb(verb="22", noun="31")
        self.computer.dsky.request_data(
            requesting_object=self._accept_thrust_fractional_part, display_location="data_2")

    def _accept_thrust_fractional_part(self, thrust):
        Program.computer.noun_data["31"][1] = thrust
        self.computer.execute_verb(verb="21", noun="38")
        self.computer.dsky.request_data(
            requesting_object=self._accept_isp, display_location="data_1")

    def _accept_isp(self, isp):
        Program.computer.noun_data["38"][0] = isp
        self.calculate_maneuver()

    def calculate_maneuver(self):
        self.update_parameters()
        self.burn = Burn(delta_v=self.delta_v,
                         direction="retrograde",
                         time_of_ignition=self.time_of_of_ignition,
                         time_of_node=self.time_of_node,
                         calling_program=self)

        self.computer.add_burn_to_queue(self.burn, execute=False)

        self.computer.execute_verb(verb="06", noun="95")
        self.computer.go_to_poo()


class Program40(Program):

    def __init__(self):
        super().__init__(description="SPS Burn", number="40")
        self.burn = self.computer.next_burn

    def execute(self):
        super().execute()

        if utils.seconds_to_time(self.burn.time_until_ignition)["minutes"] < 2:
            self.computer.remove_burn()
            self.computer.poodoo_abort(226)
            return

        if utils.seconds_to_time(self.burn.time_until_ignition)["hours"] > 0:
            utils.log("TIG > 1 hour away")
            self.computer.execute_verb(verb="16", noun="33")
            self.computer.main_loop_table.append(self._ten_minute_monitor)
        else:
            utils.log("TIG < 1 hour away, enabling burn")
            self.burn.execute()

    def _ten_minute_monitor(self):
        if utils.seconds_to_time(self.burn.time_until_ignition)["minutes"] < 10:
            self.computer.main_loop_table.remove(self._ten_minute_monitor)
            self.burn.execute()

    def terminate(self):
        super().terminate()
        self.burn.terminate()


class ProgramNotImplementedError(Exception):
    pass


programs = OrderedDict()
clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
for class_tuple in clsmembers:
    if class_tuple[0][-1].isdigit():
        programs[class_tuple[0][-2:]] = class_tuple[1]
