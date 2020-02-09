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
from src import utils, config
if config.DEBUG:
    from pudb import set_trace


class DSKY:

    dsky_instance = None

    def __init__(self, computer, ui):
        DSKY.dsky_instance = self
        self.computer = computer
        output_widgets = ui.get_output_widgets()
        self.annunciators = output_widgets[0]
        self._control_registers = output_widgets[1]
        self._data_registers = output_widgets[2]

        self.registers = {
            "program": {
                "1": self._control_registers["program"].digits[0],
                "2": self._control_registers["program"].digits[1],
            },
            "verb": {
                "1": self._control_registers["verb"].digits[0],
                "2": self._control_registers["verb"].digits[1],
            },
            "noun": {
                "1": self._control_registers["noun"].digits[0],
                "2": self._control_registers["noun"].digits[1],
            },
            "data": {
                "1": {
                    "sign": self._data_registers[1].digits[0],
                    "1": self._data_registers[1].digits[1],
                    "2": self._data_registers[1].digits[2],
                    "3": self._data_registers[1].digits[3],
                    "4": self._data_registers[1].digits[4],
                    "5": self._data_registers[1].digits[5],
                },
                "2": {
                    "sign": self._data_registers[2].digits[0],
                    "1": self._data_registers[2].digits[1],
                    "2": self._data_registers[2].digits[2],
                    "3": self._data_registers[2].digits[3],
                    "4": self._data_registers[2].digits[4],
                    "5": self._data_registers[2].digits[5],
                },
                "3": {
                    "sign": self._data_registers[3].digits[0],
                    "1": self._data_registers[3].digits[1],
                    "2": self._data_registers[3].digits[2],
                    "3": self._data_registers[3].digits[3],
                    "4": self._data_registers[3].digits[4],
                    "5": self._data_registers[3].digits[5],
                },
            },
        }

    def blank_all_registers(self):
        for register in ["verb", "noun", "program", "data_1", "data_2", "data_3"]:
            self.blank_register(register)

    def blink_register(self, register):
        for digit in self.registers[register].digits:
            digit.blink_data["is_blinking_lit"] = False
            digit.blink_data["is_blinking"] = True
            digit.display("b")

            digit.blink_timer.timeout.connect(self._blink_event)
            digit.blink_timer.start(500)

    def _blink_event(self):
        if self.is_blinking_lit:
            self.display(10)
            self.is_blinking_lit = False
        else:
            self.display(self.last_value)
            self.is_blinking_lit = True

    def blank_register(self, register):
        if isinstance(register, str):
            register = self.get_register(register)

        for digit in register.values():
            digit.display("b")

    def get_register(self, register):
        registers = {
            "verb": self.registers["verb"],
            "noun": self.registers["noun"],
            "program": self.registers["program"],
            "data_1": self.registers["data"]["1"],
            "data_2": self.registers["data"]["2"],
            "data_3": self.registers["data"]["3"],
        }
        return registers[register]

    def set_register(self, value, register, digit=None):
        if digit:
            if len(value) != 1:
                utils.log(
                    "You are trying to display a single digit, but got {} digits instead!".format(len(value)))
                return False

        else:
            if register in ["verb", "noun", "program"]:
                if not 1 <= len(value) <= 2:
                    utils.log("You are trying to display a value in the {} register, expecting 1 or 2 digits, "
                              "got {}".format(register, len(value)))
                    return False
            else:

                if not 1 <= len(value) <= 6:

                    utils.log(
                        "Must have between 1 and 6 values to display in data register, got {}".format(len(value)))
                    return False

                if value[0] not in ["+", "-", "b"]:
                    utils.log(
                        "First digit to display should be either +, -, or b, got {}".format(value[0]))
                    return False

        if register in ["verb", "noun", "program"]:
            this_register = self.get_register(register)
            if digit is not None:
                this_register[digit].display(value)
            else:
                for index in range(len(value)):
                    this_register[str(index + 1)].display(value[index])
            return True
        else:
            display_map = {
                0: "sign",
                1: "1",
                2: "2",
                3: "3",
                4: "4",
                5: "5",
            }
            if register == "data_1":
                this_register = self.registers["data"]["1"]
                if digit:
                    this_register[str(digit)].display(value)
                else:
                    for index in range(len(value)):
                        digit_to_set = display_map[index]
                        value_to_set = value[index]
                        this_register[digit_to_set].display(value_to_set)

            elif register == "data_2":
                this_register = self.registers["data"]["2"]
                if digit:
                    this_register[str(digit)].display(value)
                else:
                    for index in range(len(value)):
                        digit_to_set = display_map[index]
                        value_to_set = value[index]
                        this_register[digit_to_set].display(value_to_set)

            elif register == "data_3":
                this_register = self.registers["data"]["3"]
                if digit:
                    this_register[str(digit)].display(value)
                else:
                    for index in range(len(value)):
                        digit_to_set = display_map[index]
                        value_to_set = value[index]
                        this_register[digit_to_set].display(value_to_set)

    def set_annunciator(self, name, set_to=True):

        try:
            if set_to:
                self.annunciators[name].on()
            else:
                self.annunciators[name].off()
        except KeyError:
            utils.log(
                "You tried to change a annunciator that doesnt exist :(", "WARNING")

    def start_annunciator_blink(self, name):
        self.annunciators[name].start_blink()

    def stop_annunciator_blink(self, name):
        self.annunciators[name].stop_blink()

    def stop_comp_acty_flash(self, event):

        self.annunciators["comp_acty"].off()

    def request_data(self, requesting_object, display_location, is_proceed_available=False):
        if not is_proceed_available:
            self.blank_register(display_location)
        utils.log("{}, method {}() requesting data".format(
            requesting_object.__self__, requesting_object.__name__))
        self.verb_noun_flash_on()
        self.computer.keyboard_state["object_requesting_data"] = requesting_object
        self.computer.keyboard_state["is_expecting_data"] = True
        self.computer.keyboard_state["display_location_to_load"] = display_location

    def verb_noun_flash_on(self):

        self.registers["verb"]["1"].start_blink()
        self.registers["verb"]["2"].start_blink()
        self.registers["noun"]["1"].start_blink()
        self.registers["noun"]["2"].start_blink()

    def verb_noun_flash_off(self):

        self.registers["verb"]["1"].stop_blink()
        self.registers["verb"]["2"].stop_blink()
        self.registers["noun"]["1"].stop_blink()
        self.registers["noun"]["2"].stop_blink()

    def stop_blink(self):
        utils.log(
            message="Called depreciated method stop_blink(). Please use verb_noun_flash_off()", log_level="ERROR")

    def flash_comp_acty(self):
        """ Flashes the COMP ACTY annunciator.
        """
        pass

    def reset_annunciators(self):

        for annunciator in self.annunciators:
            self.annunciators[annunciator].off()

    def set_tooltip(self, register, tooltip):
        this_register = self.get_register(register)
        for digit in this_register.values():
            digit.set_tooltip(tooltip)
