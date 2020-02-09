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
import math


from pudb import set_trace

from src import config, telemachus, utils
from src.config import TELEMACHUS_BODY_IDS
from src.telemachus import get_telemetry

if config.DEBUG:
    from pudb import set_trace

computer = None

class HohmannTransfer:

    def __init__(self):
        self.delta_v_1 = 0.0
        self.delta_v_2 = 0.0
        self.orbiting_body = get_telemetry("body")
        self.radius = get_telemetry("body_radius", body_number=config.TELEMACHUS_BODY_IDS[self.orbiting_body])
        
        self.phase_angle_required = 0.0
        self.time_of_ignition_first_burn = 0.0
        self.target_name = "Mun"
        self.departure_body = get_telemetry("body")
        self.departure_altitude = get_telemetry("sma")
        self.radius = get_telemetry("body_radius", body_number=config.TELEMACHUS_BODY_IDS[self.orbiting_body])
        self.destination_altitude = 13500000 + self.radius
        self.grav_param = get_telemetry("body_gravParameter",
                                         body_number=config.TELEMACHUS_BODY_IDS[self.orbiting_body])
        
        self.orbital_period = get_telemetry("period")
        self.departure_body_period = get_telemetry("body_period",
                                                    body_number=config.TELEMACHUS_BODY_IDS["Kerbin"])
        self.first_burn = None
        self.second_burn = None
        self.target_id = config.TELEMACHUS_BODY_IDS[self.target_name]

        self.time_of_node = 0.0
        self.duration_of_burn = 0

    def calculate_sma_transfer_ellipse(self):
        
        radius_departure_orbit = self.departure_altitude
        radius_arrival_orbit = self.destination_altitude
        sma = (radius_departure_orbit + radius_arrival_orbit) / 2
        return sma

    def calculate_velocity_initial(self):
        
        radius_departure_orbit = self.departure_altitude
        vi = math.sqrt(self.grav_param / radius_departure_orbit)
        return vi

    def calculate_velocity_final(self):
        radius_arrival_orbit = self.destination_altitude
        vf = math.sqrt(self.grav_param / radius_arrival_orbit)
        return vf

    def calculate_velocity_initial_on_transfer_orbit(self):
        radius_departure_orbit = self.departure_altitude
        vtxi = math.sqrt(self.grav_param * ((2 / radius_departure_orbit) - (1 / self.calculate_sma_transfer_ellipse())))
        return vtxi

    def calculate_velocity_final_on_transfer_orbit(self):
        radius_arrival_orbit = self.destination_altitude
        vtxf = math.sqrt(self.grav_param * ((2 / radius_arrival_orbit) - (1 / self.calculate_sma_transfer_ellipse())))
        return vtxf

    def calculate_initial_delta_v(self):
        return self.calculate_velocity_initial_on_transfer_orbit() - self.calculate_velocity_initial()

    def calculate_final_delta_v(self):
        return self.calculate_velocity_final() - self.calculate_velocity_final_on_transfer_orbit()

    def calculate_total_delta_v(self):
        return self.calculate_initial_delta_v() + self.calculate_final_delta_v()
        
    def calculate_other_parameters(self):
        utils.log("Initial velocity at start of transfer: {:.2f} m/s".format(self.calculate_velocity_initial()))
        utils.log("Velocity on transfer orbit at initial orbit: {:.2f} m/s".format(self.calculate_velocity_initial_on_transfer_orbit()))
        utils.log("Velocity on transfer orbit at final orbit: {:.2f} m/s".format(self.calculate_velocity_final_on_transfer_orbit()))
        utils.log("Initial velocity change (delta-v): {:.2f} m/s".format(self.calculate_initial_delta_v()))
        utils.log("Final velocity change (delta-v): {:.2f} m/s".format(self.calculate_final_delta_v()))
        utils.log("Total chance in velocity (delta-v): {:.2f} m/s".format(self.calculate_total_delta_v()))
        utils.log()
            
    @staticmethod
    def check_orbital_parameters():
        
        if get_telemetry("eccentricity") > 0.002:
            return (False, 224)


        target_inclination = get_telemetry("target_inclination")
        vessel_inclination = get_telemetry("inclination")
        if (vessel_inclination > (target_inclination - 1)) and (vessel_inclination > (target_inclination + 1)):

            return (False, 225)
        else:
            return True

    def update_parameters(self):


        self.departure_altitude = get_telemetry("altitude")
        self.calculate()
        self.calculate_burn_timings()
        self.first_burn.delta_v = self.delta_v_1
        self.first_burn.time_of_ignition = self.time_of_ignition_first_burn
        self.first_burn.time_of_node = self.time_of_node
        telemachus.update_maneuver_node(ut=self.time_of_node, delta_v=(0.0, 0.0, self.delta_v_1))
        if config.current_log_level == "DEBUG":
            self.print_maneuver_data()

    def print_maneuver_data(self):
        self.calculate_other_parameters()
        utils.log("-" * 40)
        utils.log("Hohmann Transfer Data:")
        utils.log("Delta-V required: {:.2f}".format(self.delta_v_1))
        utils.log("Phase angle required: {:.2f}".format(self.phase_angle_required))
        utils.log("Burn duration: {:.2f} seconds".format(self.duration_of_burn))
        utils.log("-" * 40)

    def execute(self):

        self.calculate()
        time_to_node = HohmannTransfer.get_time_to_node(self.phase_angle_difference(),
                                                                     self.orbital_period,
                                                                     self.departure_body_period)
        if time_to_node <= 120:
            utils.log("Time of ignition less that 2 minutes in the future, starting burn during next orbit")
            time_to_node += self.orbital_period
        self.calculate_burn_timings()
        self.first_burn = Burn(delta_v=self.delta_v_1,
                               direction="node",
                               time_of_ignition=self.time_of_ignition_first_burn,
                               time_of_node=self.time_of_node,
                               burn_duration=self.duration_of_burn,
                               )
        if config.current_log_level == "DEBUG":
            self.print_maneuver_data()
        computer.add_burn(self.first_burn)

    def phase_angle_difference(self):

        current_phase_angle = get_telemetry("body_phaseAngle", body_number=self.target_id)
        phase_angle_difference = current_phase_angle - self.phase_angle_required
        utils.log()
        utils.log("Current Phase Angle: {} degrees".format(current_phase_angle))
        utils.log("Phase Angle Required: {} degrees".format(self.phase_angle_required))
        utils.log("Phase Angle Difference: {} degrees".format(phase_angle_difference))
        return phase_angle_difference
        
    def calculate(self):


        self.phase_angle_required = HohmannTransfer.calculate_phase_angle(
            self.departure_altitude,
            self.destination_altitude,
            self.grav_param,
        )


        self.delta_v_1, self.delta_v_2 = HohmannTransfer.calculate_delta_v(self.departure_altitude,
                                                                   self.destination_altitude)

        self.time_to_transfer = HohmannTransfer.time_to_transfer(self.departure_altitude,
                                                 self.destination_altitude,
                                                 self.grav_param)



    def calculate_burn_timings(self):
        time_to_node = HohmannTransfer.get_time_to_node(self.phase_angle_difference(),
                                                                     self.orbital_period,
                                                                     self.departure_body_period)

        self.time_of_node = get_telemetry("universalTime") + time_to_node
        initial_mass = float(computer.noun_data["25"][0] + "." + computer.noun_data["25"][1])
        thrust = float(computer.noun_data["31"][0] + "." + computer.noun_data["31"][1])
        specific_impulse = float(computer.noun_data["38"][0])
        self.duration_of_burn = calc_burn_duration(initial_mass, thrust, specific_impulse, self.delta_v_1)
        self.time_of_ignition_first_burn = self.time_of_node - (self.duration_of_burn / 2) 
    
    @staticmethod
    def get_time_to_node(phase_angle_difference, orbital_period, departure_orbital_period):
        tig = phase_angle_difference / ((360 / orbital_period) - (360 / departure_orbital_period))
        if tig < 0:
            utils.log("Setting node at next orbit")
            tig += orbital_period
        return tig
        
    @staticmethod
    def time_to_transfer(departure_orbit, destination_orbit, grav_param):
        tH = math.pi * math.sqrt(math.pow(departure_orbit + destination_orbit, 3) / (8 * grav_param))
        return tH

    @staticmethod
    def calculate_phase_angle(departure_orbit, destination_orbit, grav_param):
        tH = HohmannTransfer.time_to_transfer(departure_orbit, destination_orbit, grav_param)
        required_phase_angle = 180 - math.sqrt(grav_param / destination_orbit) * (tH / destination_orbit) * 180 / math.pi
        return required_phase_angle

    @staticmethod
    def calculate_delta_v(departure_altitude, destination_altitude, departure_body="Kerbin"):
        r1 = departure_altitude
        r2 = destination_altitude
        mu = float(get_telemetry("body_gravParameter", body_number=TELEMACHUS_BODY_IDS[departure_body]))
        sqrt_r1 = math.sqrt(r1)
        sqrt_r2 = math.sqrt(r2)
        sqrt_2_sum = math.sqrt(2 / (r1 + r2))
        sqrt_mu = math.sqrt(mu)
        delta_v_1 = sqrt_mu / sqrt_r1 * (sqrt_r2 * sqrt_2_sum - 1)
        delta_v_2 = sqrt_mu / sqrt_r2 * (1 - sqrt_r1 * sqrt_2_sum)
        return delta_v_1, delta_v_2


class Burn:

    def __init__(self, delta_v, direction, time_of_ignition, time_of_node, burn_duration, recalc_function=None):

        self.burn_duration = burn_duration
        self.recalc_function = recalc_function
        self.delta_v_required = delta_v
        self.direction = direction
        self.time_of_ignition = time_of_ignition
        self.time_of_node = time_of_node
        self.time_until_ignition = self.calculate_time_to_ignition()
        
        self.is_display_blanked = False
        self.is_verb_99_executed = False
        
        self.is_directional_autopilot_engaged = False
        self.is_thrust_autopilot_engaged = False
        self.is_active = False
        
        self.initial_speed = 0.0
        self.accumulated_delta_v = 0.0
        self._is_thrust_reduced = False
        self.current_velocity = 0.0

    def recalculate(self):
        self.recalc_function()
        self.time_until_ignition = self.calculate_time_to_ignition()
        self.velocity_at_cutoff = self._calculate_velocity_at_cutoff()
    
    def execute(self):

        self.add_maneuver_node()
        computer.main_loop_table.append(self._coarse_start_time_monitor)
        computer.execute_verb(verb="16", noun="40")
        
    def add_maneuver_node(self):

        telemachus.add_maneuver_node(ut=self.time_of_node, delta_v=(0.0, 0.0, self.delta_v_required))
        
    def terminate(self):
        self._disable_directional_autopilot()


        telemachus.cut_throttle()
        computer.remove_burn()

    def _coarse_start_time_monitor(self):

        self.time_until_ignition = self.calculate_time_to_ignition()


        if int(self.time_until_ignition) == 105 and not self.is_display_blanked:

            computer.dsky.current_verb.terminate()
            for register in ["verb", "noun", "program", "data_1", "data_2", "data_3"]:
                computer.dsky.blank_register(register)
            self.is_display_blanked = True

        if int(self.time_until_ignition) <= 100 and self.is_display_blanked:

            computer.dsky.set_register(computer.running_program.number, "program")
            computer.execute_verb(verb="16", noun="40")
            self.is_display_blanked = False
            self._enable_directional_autopilot()


        if int(self.time_until_ignition) <= 10:
            computer.main_loop_table.remove(self._coarse_start_time_monitor)
            computer.execute_verb(verb="99", object_requesting_proceed=self._accept_enable_engine)

    def _accept_enable_engine(self, data):
        if data == "proceed":
            utils.log("Go for burn!", log_level="INFO")
        else:
            return
        computer.main_loop_table.append(self._fine_start_time_monitor)
        computer.execute_verb(verb="16", noun="40")

    def _fine_start_time_monitor(self):

        self.time_until_ignition = self.calculate_time_to_ignition()
        if float(self.time_until_ignition) < 1.1:  
            utils.log("Engine Ignition", log_level="INFO")
            self._begin_burn()
            computer.main_loop_table.remove(self._fine_start_time_monitor)

    def _begin_burn(self):

        self.initial_speed = get_telemetry("orbitalVelocity")
        self.velocity_at_cutoff = self._calculate_velocity_at_cutoff()

        telemachus.set_throttle(100)
        computer.main_loop_table.append(self._thrust_monitor)

    
    def _thrust_monitor(self):

        self.accumulated_delta_v = self._calculate_accumulated_delta_v()
        current_velocity = get_telemetry("orbitalVelocity")


        if current_velocity > (self.velocity_at_cutoff - 13.5) and not self._is_thrust_reduced:
            utils.log("Throttling back to 10%", log_level="DEBUG")
            telemachus.set_throttle(10)
            self._is_thrust_reduced = True
            telemachus.disable_smartass()
            telemachus.send_command_to_ksp("command=f.sas")

        if current_velocity > (self.velocity_at_cutoff - 3.5): 
            telemachus.cut_throttle()
            utils.log("Closing throttle, burn complete!", log_level="DEBUG")
            computer.dsky.current_verb.terminate()
            computer.execute_verb(verb="06", noun="14")
            computer.main_loop_table.remove(self._thrust_monitor)
            self.terminate()
            computer.go_to_poo()


    def _calculate_velocity_at_cutoff(self):
        return self.initial_speed + self.delta_v_required

    def calculate_time_to_ignition(self):
        current_time = get_telemetry("universalTime")
        return self.time_of_ignition - current_time

    def _calculate_accumulated_delta_v(self):
        current_speed = get_telemetry("orbitalVelocity")
        return current_speed - self.initial_speed

    def _disable_directional_autopilot(self):

        telemachus.disable_smartass()
        utils.log("Directional autopilot disabled", log_level="INFO")
        return True

    def _enable_directional_autopilot(self):
        
        telemachus.set_mechjeb_smartass("node")
        utils.log("Directional autopilot enabled", log_level="INFO")
        return True

def calc_burn_duration(initial_mass, thrust, specific_impulse, delta_v):
    exhaust_velocity = specific_impulse * 9.81
    burn_duration = (initial_mass * exhaust_velocity / thrust) * (1 - math.exp(-delta_v / exhaust_velocity))
    utils.log(log_level="info")
    utils.log("-" * 40, log_level="info")
    utils.log("Burn duration calculations:", log_level="info")
    utils.log("Initial mass: {} tonnes".format(initial_mass), log_level="info")
    utils.log("Thrust: {} kN".format(thrust), log_level="info")
    utils.log("Specific Impulse: {} seconds".format(specific_impulse), log_level="info")
    utils.log("Exhaust Velocity: {:.2f} kg/s".format(exhaust_velocity), log_level="info")
    utils.log("Burn Duration: {:.1f} seconds".format(burn_duration), log_level="info")
    utils.log("-" * 40, log_level="info")
    return burn_duration
