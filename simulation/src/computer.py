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
from src import maneuver
from src import imu
from src import verbs
from src import utils
from src import telemachus
from src import routines
from src import programs
from src import nouns
from src import dsky
import os
from PyQt5.QtCore import QTimer
from src import config
if config.DEBUG:
    from pudb import set_trace


class Computer:
    computer_instance = None

    def __init__(self, ui):
        Computer.computer_instance = self
        verbs.Verb.computer = self
        programs.Program.computer = self
        nouns.computer = self
        maneuver.computer = self

        self.ui = ui
        self.dsky = dsky.DSKY(self, self.ui)
        self.imu = imu.IMU(self)

        self.keyboard_state = {
            "input_data_buffer": "",
            "register_index": 0,
            "is_verb_being_loaded": False,
            "is_noun_being_loaded": False,
            "is_data_being_loaded": False,
            "verb_position": 0,
            "noun_position": 0,
            "requested_verb": "",
            "requested_noun": "",
            "current_verb": 0,
            "current_noun": 0,
            "current_program": 0,
            "display_lock": None,
            "backgrounded_update": None,
            "is_expecting_data": False,
            "is_expecting_proceed": False,
            "object_requesting_data": None,
            "display_location_to_load": None,
            "set_keyboard_state_setter": self.set_keyboard_state,
        }
        self.main_loop_timer = QTimer()
        self.main_loop_timer.timeout.connect(self.main_loop)

        self.slow_loop_timer = QTimer()
        self.slow_loop_timer.timeout.connect(self.slow_loop)

        self.comp_acty_timer = QTimer()
        self.comp_acty_timer.timeout.connect(self._comp_acty_off)

        self.uplink_queue = []
        self.is_powered_on = False
        self.main_loop_table = []
        self.alarm_codes = [0, 0, 0]
        self.running_programs = []
        self.noun_data = {
            "30": ["00002"],
            "25": ["00000", "00000", ""],
            "31": ["00000", "00000"],
            "38": ["00000", "", ""],
        }
        self.next_burn = None
        self.is_ksp_connected = False
        self.ksp_paused_state = None
        self.is_direction_autopilot_engaged = False
        self.is_thrust_autopilot_engaged = False
        self.moi_burn_delta_v = 0.0

        self.nouns = nouns.nouns
        self.verbs = verbs.verbs
        self.programs = programs.programs

        self.option_codes = {
            "00001": "",
            "00002": "",
            "00003": "",
            "00004": "",
            "00007": "",
            "00024": "",
        }
        self.register_charin()
        self.on()

    def accept_uplink(self):
        try:
            uplink_file = open(os.path.join(
                config.BASE_DIR, "src/", "uplink.txt"), "r")
        except FileNotFoundError:
            self.program_alarm(501)
            return
        self.dsky.set_annunciator("uplink_acty")
        uplink_data = uplink_file.read().strip()
        uplink_file.close()
        for char in uplink_data:
            if char == "\n":
                continue
            self.uplink_queue.append(char)

    def charin(self, keypress):
        routines.charin(keypress, self.keyboard_state, self.dsky, self)

    def process_uplink_data(self):
        if len(self.uplink_queue) > 0:
            char = self.uplink_queue.pop(0)
            self.charin(char)
            return True
        else:
            self.dsky.set_annunciator("uplink_acty", False)
            return False

    def add_to_mainloop(self, func):
        self.main_loop_table.append(func)

    def remove_from_mainloop(self, func):
        if func in self.main_loop_table:
            self.main_loop_table.remove(func)
        else:
            utils.log(
                "Cannot remove function from mainloop, function {} not found".format(func))

    def register_charin(self):
        self.ui.register_key_event_handler(self.charin)

    def set_keyboard_state(self, state_name, new_value):
        self.keyboard_state[state_name] = new_value

    def add_burn(self, burn_object):
        self.next_burn = burn_object

    def enable_burn(self):
        self.next_burn.execute()

    def remove_burn(self):
        self.next_burn = None

    def disable_direction_autopilot(self):
        telemachus.disable_smartass()
        self.is_direction_autopilot_engaged = False
        utils.log("Autopilot disabled", log_level="INFO")

    def quit(self):
        try:
            telemachus.disable_smartass()
        except TypeError:
            pass
        self.gui.Destroy()

    def on(self):
        utils.log("Computer booting...", log_level="INFO")
        try:
            telemachus.get_api_listing()
        except telemachus.KSPNotConnected:
            utils.log(
                "Cannot retrieve telemetry listing - no connection to KSP", log_level="WARNING")
        else:
            utils.log("Retrieved telemetry listing", log_level="INFO")
        self.add_to_mainloop(self.process_uplink_data)

        self.main_loop_timer.start(config.LOOP_TIMER_INTERVAL)
        self.slow_loop_timer.start(config.SLOW_LOOP_TIMER_INTERVAL)
        self.is_powered_on = True

    def main_loop(self):
        for item in self.main_loop_table:
            item()

    def slow_loop(self):
        if not telemachus.check_connection():
            self.dsky.annunciators["no_att"].on()
        if config.ENABLE_COMP_ACTY_FLASH:
            self.flash_comp_acty()

    def go_to_poo(self):
        poo = self.programs["00"]()
        poo.execute()

    def execute_verb(self, verb=None, noun=None, **kwargs):
        if not verb:
            verb = self.keyboard_state["requested_verb"]
        self.dsky.set_register(value=verb, register="verb")

        if not noun:
            try:
                if self.keyboard_state["requested_noun"] == "":
                    verb_to_execute = self.verbs[verb](**kwargs)
                else:
                    print(self.keyboard_state["requested_noun"])
                    verb_to_execute = self.verbs[verb](
                        self.keyboard_state["requested_noun"], **kwargs)
            except KeyError:
                self.operator_error("Verb {} does not exist :(".format(verb))
                return
        else:
            verb_to_execute = self.verbs[verb](noun, **kwargs)

        self.flash_comp_acty(200)
        verb_to_execute.execute()

    def execute_program(self, program_number):
        try:
            program = self.programs[program_number]()
        except KeyError:
            self.program_alarm(116)
            self.go_to_poo()
            return
        program.execute()

    def flash_comp_acty(self, duration=config.COMP_ACTY_FLASH_DURATION):
        self.dsky.annunciators["comp_acty"].on()
        self.comp_acty_timer.start(duration)

    def _comp_acty_off(self):
        self.dsky.annunciators["comp_acty"].off()
        self.comp_acty_timer.stop()

    def operator_error(self, message=None):
        if message:
            utils.log("OPERATOR ERROR: " + message, log_level="ERROR")
        self.dsky.annunciators["opr_err"].blink_timer.start(500)

    def reset_alarm_codes(self):
        self.alarm_codes[2] = self.alarm_codes[0]
        self.alarm_codes[0] = 0
        self.alarm_codes[1] = 0

    def program_alarm(self, alarm_code):
        utils.log("PROGRAM ALARM {}: {}".format(str(alarm_code),
                                                config.ALARM_CODES[alarm_code]), log_level="ERROR")
        alarm_code += 1000
        if self.alarm_codes[0] != 0:
            self.alarm_codes[1] = self.alarm_codes[0]
        self.alarm_codes[0] = alarm_code
        self.alarm_codes[2] = self.alarm_codes[0]
        self.dsky.annunciators["prog"].on()

    def poodoo_abort(self, alarm_code, message=None):
        alarm_code += 2000
        if self.alarm_codes[0] != 0:
            self.alarm_codes[1] = self.alarm_codes[0]
        self.alarm_codes[0] = alarm_code
        self.alarm_codes[2] = self.alarm_codes[0]
        self.dsky.annunciators["prog"].on()
        self.running_program.terminate()
        utils.log("P00DOO ABORT {}: {}".format(
            str(alarm_code), message), log_level="ERROR")
        poo = self.programs["00"]()
        poo.execute()

    def program_restart(self, alarm_code, message=None):
        utils.log("Program fresh start not implemented yet... watch this space...")
        if message:
            utils.log(message, log_level="ERROR")

    def computer_restart(self, alarm_code, message=None):
        if message:
            utils.log(message, log_level="CRITICAL")
        pass

    def servicer(self):
        """
        The servicer updates the spacecrafts state vector.
        """
        pass
