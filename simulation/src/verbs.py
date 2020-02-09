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
import inspect
import logging
import sys
from collections import OrderedDict

from PyQt5.QtCore import QTimer
from src import config, nouns, utils, dsky
from src.telemachus import KSPNotConnected, TelemetryNotAvailable
from src import telemachus
if config.DEBUG:
    from pudb import set_trace

log = logging.getLogger("Verbs")

INVALID_VERBS = [
    0,
    8,
    9,
    10,
    18,
    19,
    20,
    26,
    28,
    29,
    38,
    39,
    68,
    76,
    77,
    79,
    84,
    95,
    98,
]


class NounNotAcceptableError(Exception):

    """ This exception is raised when the noun selected is not available with the verb selected."""
    pass

class Verb:


    computer = None
    
    def __init__(self, name, verb_number, noun=None):
        
        self.computer = Verb.computer
        self.dsky = dsky.DSKY.dsky_instance
        self.name = name
        self.number = verb_number
        self.illegal_nouns = []
        self.data = []
        self.noun = noun

    def _format_output_data(self, data):


        raw_data = [data[1], data[2], data[3]]
        out_data = []
        for item in raw_data:
            if not item:
                continue
            output = ""
            if data["is_octal"]:
                output = "b"
                output += item.zfill(5)
            elif item[0] == "-":
                output += item.zfill(6)
            else:
                output = "+"
                output += item.zfill(5)
            out_data.append(output)
        return out_data

    def execute(self):


        if self.noun in self.illegal_nouns:
            raise NounNotAcceptableError
        utils.log("Executing Verb {}: {}".format(self.number, self.name))
        self.dsky.current_verb = self
        if self.noun:
            Verb.computer.dsky.set_register(self.noun, "noun")
            utils.log(" With noun {}".format(self.noun)) # JRI

    def terminate(self):

  

        Verb.computer.dsky.current_verb = None

    def receive_data(self, data):


        utils.log("{} received data: {}".format(self, data))
        self.data = data
        self.execute()

    def __str__(self):
        return "Verb {} ({})".format(self.number, self.name)


class ExtendedVerb(Verb):


    def __init__(self, name, verb_number):

        super().__init__(name, verb_number, noun=None)


class DisplayVerb(Verb):

    def __init__(self, name, verb_number, noun):


        super().__init__(name, verb_number, noun)

    def execute(self):


        super(DisplayVerb, self).execute()



class MonitorVerb(DisplayVerb):

 

    def __init__(self, name, verb_number, noun):

        super().__init__(name, verb_number, noun)
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_display)
        self.is_tooltips_set = False

    def _send_output(self):
        if self.timer.interval() != config.DISPLAY_UPDATE_INTERVAL:
            self.timer.stop()
            self.timer.start(config.DISPLAY_UPDATE_INTERVAL)

        if self.noun is None:
            self.noun = Verb.computer.keyboard_state["requested_noun"]
        if self.noun in self.illegal_nouns:
            raise NounNotAcceptableError
        noun_function = Verb.computer.nouns[self.noun]()
        try:
            data = noun_function.return_data()
        except nouns.NounNotImplementedError:
            self.computer.operator_error("Noun {} not implemented yet. Sorry about that...".format(self.noun))
            self.terminate()
            return
        except KSPNotConnected:
            utils.log("KSP not connected, terminating V{}".format(self.number),
                      log_level="ERROR")
            Verb.computer.program_alarm(110)
            self.terminate()
            raise
        except TelemetryNotAvailable:
            utils.log("Telemetry not available, terminating V{}".format(self.number),
                      log_level="ERROR")
            Verb.computer.program_alarm(111)
            self.terminate()
            raise
        if not data:

            self.terminate()
            return
        output = self._format_output_data(data)

        if not self.is_tooltips_set:
            Verb.computer.dsky.set_tooltip("data_1", data["tooltips"][0])
            Verb.computer.dsky.set_tooltip("data_2", data["tooltips"][1])
            Verb.computer.dsky.set_tooltip("data_3", data["tooltips"][2])

            self.is_tooltips_set = True

        Verb.computer.dsky.set_register(output[0], "data_1")
        Verb.computer.dsky.set_register(output[1], "data_2")
        Verb.computer.dsky.set_register(output[2], "data_3")

        Verb.computer.dsky.flash_comp_acty()

    def start_monitor(self):
        Verb.computer.keyboard_state["display_lock"] = self

        try:
            self._send_output()
        except KSPNotConnected:
            return
        except TelemetryNotAvailable:
            return
        if self.noun is None:
            return

        self.timer.start(config.DISPLAY_UPDATE_INTERVAL)

    def _update_display(self):
        self._send_output()

    def terminate(self):

        utils.log("Terminating V{}".format(self.number))
        Verb.computer.dsky.stop_annunciator_blink("key_rel")
        Verb.computer.keyboard_state["display_lock"] = None
        Verb.computer.keyboard_state["backgrounded_update"] = None
        self.timer.stop()
        self.noun = None

        Verb.computer.dsky.set_tooltip("data_1", "")
        Verb.computer.dsky.set_tooltip("data_2", "")
        Verb.computer.dsky.set_tooltip("data_3", "")

    def background(self):


        Verb.computer.keyboard_state["backgrounded_update"] = self
        Verb.computer.keyboard_state["display_lock"] = None
        self.timer.stop()
        Verb.computer.dsky.start_annunciator_blink("key_rel")
        

    def resume(self):

        Verb.computer.keyboard_state["display_lock"] = self
        Verb.computer.keyboard_state["backgrounded_update"] = None
        Verb.computer.dsky.set_register(self.number, "verb")
        Verb.computer.dsky.set_register(self.noun, "noun") 
    
        self.start_monitor()


class LoadVerb(Verb):



    def __init__(self, name, verb_number, noun):

        super().__init__(name, verb_number, noun)

    def accept_input(self, data):

        Verb.computer.noun_data[self.noun][21 - int(self.number)] = data


class Verb01(DisplayVerb):


    def __init__(self, noun):

  

        super().__init__(name="Display Octal component 1 in R1", verb_number="01", noun=noun)
        
    def execute(self):

  
        
        super().execute()
        noun_function = Verb.computer.nouns[self.noun]()
        noun_data = noun_function.return_data()
        if noun_data is False:
            return
        output = self._format_output_data(noun_data)
        Verb.computer.dsky.set_register(output[0], "data_1")


class Verb02(DisplayVerb):


    def __init__(self, noun):



        super().__init__(name="Display Octal component 2 in R1", verb_number="02", noun=noun)
        
    def execute(self):


        super().execute()
        noun_function = Verb.computer.nouns[self.noun]()
        noun_data = noun_function.return_data()
        if noun_data is False:

            return
        output = self._format_output_data(noun_data)
        Verb.computer.dsky.set_register(output[1], "data_2")

class Verb03(DisplayVerb):

 

    def __init__(self, noun):



        super().__init__(name="Display Octal component 3 in R1", verb_number="03", noun=noun)
        
    def execute(self):



        super().execute()
        noun_function = Verb.computer.nouns[self.noun]()
        noun_data = noun_function.return_data()
        if noun_data is False:
            return
        output = self._format_output_data(noun_data)
        Verb.computer.dsky.set_register(output[2], "data_3")

class Verb04(DisplayVerb):


    def __init__(self, noun):


        super().__init__(name="Display Octal components 1, 2 in R1, R2", verb_number="04", noun=noun)

    def execute(self):



        super().execute()
        noun_function = Verb.computer.nouns[Verb.computer.dsky.state["requested_noun"]]
        noun_data = noun_function(calling_verb=self)
        output = self._format_output_data(noun_data)
        Verb.computer.dsky.set_register(output[0], "data_1")
        Verb.computer.dsky.set_register(output[1], "data_2")


class Verb05(DisplayVerb):

    def __init__(self, noun):



        super().__init__(name="Display Octal components 1, 2, 3 in R1, R2, R3", verb_number="05", noun=noun)
        self.illegal_nouns = []

    def execute(self):


        super().execute()
        noun_function = Verb.computer.nouns[Verb.computer.keyboard_state["requested_noun"]]()
        noun_data = noun_function.return_data()
        if not noun_data:

            return
        output = self._format_output_data(noun_data)
        Verb.computer.dsky.set_register(output[0], "data_1")
        Verb.computer.dsky.set_register(output[1], "data_2")
        Verb.computer.dsky.set_register(output[2], "data_3")


class Verb06(DisplayVerb):

    def __init__(self, noun):


        super().__init__(name="Display Decimal in R1 or in R1, R2 or in R1, R2, R3", verb_number="06",
                                    noun=noun)

    def execute(self):

  

        super().execute()
        noun_function = Verb.computer.nouns[self.noun]()
        noun_data = noun_function.return_data()
        if not noun_data:
            return
        output = self._format_output_data(noun_data)

        
        Verb.computer.dsky.set_tooltip("data_1", noun_data["tooltips"][0])
        Verb.computer.dsky.set_tooltip("data_2", noun_data["tooltips"][1])
        Verb.computer.dsky.set_tooltip("data_3", noun_data["tooltips"][2])
        Verb.computer.dsky.set_register(output[0], "data_1")
        Verb.computer.dsky.set_register(output[1], "data_2")
        Verb.computer.dsky.set_register(output[2], "data_3")



class Verb11(MonitorVerb):



    def __init__(self, noun):


        super().__init__(name="Monitor Octal component 1 in R1", verb_number="11", noun=noun)


class Verb12(MonitorVerb):


    def __init__(self, noun):



        super().__init__(name="Monitor Octal component 2 in R1", verb_number="12", noun=noun)


class Verb13(MonitorVerb):

  

    def __init__(self, noun):

 

        super().__init__(name="Monitor Octal component 3 in R1", verb_number="13", noun=noun)


class Verb14(MonitorVerb):


    def __init__(self, noun):



        super().__init__(name="Monitor Octal components 1, 2 in R1, R2", verb_number="14", noun=noun)


class Verb15(MonitorVerb):



    def __init__(self, noun):

        super().__init__(name="Monitor Octal components 1, 2, 3 in R1, R2, R3", verb_number="15", noun=noun)


class Verb16(MonitorVerb):

 

    def __init__(self, noun):



        super().__init__(name="Monitor Decimal in R1 or in R1, R2 or in R1, R2, R3", verb_number="16", noun=noun)

    def execute(self):

        super().execute()
        self.start_monitor()


class Verb17(MonitorVerb):



    def __init__(self, noun):


        super().__init__(name="Monitor Double Precision Decimal in R1, R2 (test only)", verb_number="17",
                                     noun=noun)



class Verb21(LoadVerb):


    def __init__(self, noun):


        super().__init__(name="Load component 1 into R1", verb_number="21", noun=noun)

    def execute(self):

 
        super().execute()
        Verb.computer.dsky.request_data(self.accept_input, display_location="data_1")


class Verb22(LoadVerb):

 

    def __init__(self, noun):


        super().__init__(name="Load component 2 into R2", verb_number="22", noun=noun)

    def execute(self):

        super().execute()
        Verb.computer.dsky.request_data(self.accept_input, display_location="data_2")


class Verb23(LoadVerb):

    def __init__(self, noun):



        super().__init__(name="Load component 3 into R3", verb_number="23", noun=noun)

    def execute(self):


        super().execute()
        Verb.computer.dsky.request_data(self.accept_input, display_location="data_3")



class Verb34(Verb):


    def __init__(self):


        super().__init__(name="Terminate function", verb_number="34")

    def execute(self):


        if Verb.computer.keyboard_state["backgrounded_update"]:
            utils.log("Terminating backgrounded update")
            Verb.computer.keyboard_state["backgrounded_update"].terminate()
            Verb.computer.dsky.stop_annunciator_blink("key_rel")
        if Verb.computer.running_program:
            utils.log("Terminating active program {}".format(Verb.computer.running_program.number))
            Verb.computer.running_program.terminate()
        else:
            utils.log("V34 called, but nothing to terminate!")


class Verb35(Verb):



    def __init__(self):



        super().__init__(name="Test lights", verb_number="35")
        self.flash_timer = QTimer()

    def execute(self):



        for annunciator in self.dsky.annunciators.values():
            annunciator.on()

        for register in ["1", "2", "3"]:
            self.dsky.set_register(value="+88888", register="data_{}".format(register))

        for register in ["verb", "noun", "program"]:
            self.dsky.set_register(value="88", register=register)

        self.dsky.verb_noun_flash_on()
        self.dsky.start_annunciator_blink("opr_err")
        self.dsky.start_annunciator_blink("key_rel")
        self.flash_timer.singleShot(5000, self.terminate)
        self.computer.flash_comp_acty(500)
        self.computer.memory_hack = self
        
    def terminate(self):

        for annunciator in self.dsky.annunciators.values():
            annunciator.off()
        self.dsky.verb_noun_flash_off()
        self.dsky.set_register("88", "verb")
        self.dsky.set_register("88", "noun")
        self.dsky.stop_annunciator_blink("opr_err")
        self.dsky.stop_annunciator_blink("key_rel")
        self.dsky.set_register(value="bb", register="program")
        self.computer.memory_hack = None
        

class Verb36(Verb):


    def __init__(self, noun):


        super().__init__(name="Request fresh start", verb_number="36", noun=noun)

    def execute(self):


        Verb.computer.fresh_start()


class Verb37(Verb):


    def __init__(self):

        super().__init__(name="Change program (Major Mode)", verb_number="37")

    def execute(self):

        super().execute()
        self.dsky.request_data(requesting_object=self.receive_data, display_location="noun")

    def receive_data(self, data):

        if len(data) != 2:
            self.computer.operator_error("Expected exactly two digits, received {} digits".format(len(data)))
            self.terminate()
            return
        Verb.computer.execute_program(data)

class Verb75(ExtendedVerb):

 
    def __init__(self):


        super().__init__(name="Backup liftoff", verb_number="75")

    def execute(self):


        program = Verb.computer.programs["11"]()
        program.execute()


class Verb82(ExtendedVerb):



    def __init__(self):

     

        super().__init__(name="Request orbital parameters display (R30)", verb_number="82")

    def execute(self):

        Verb.computer.execute_verb(verb="16", noun="44")


class Verb93(ExtendedVerb):


    
    def __init__(self):
        

        
        super().__init__(name="Disable Autopilot", verb_number="93")

    def execute(self):
        

        
        Verb.computer.disable_direction_autopilot()


class Verb98(ExtendedVerb):

    def __init__(self):

        super().__init__(name="Debug", verb_number="98")

    def execute(self):
        

        super().execute()
        self.dsky.request_data(requesting_object=self.receive_data, display_location="noun")

    def receive_data(self, data):

        if data == "01":
            Verb.computer.accept_uplink()
        elif data == "02":
            data = telemachus.get_telemetry("maneuverNodes")
            data = data[0]
            for key, value in sorted(data.items()):
                if key == "orbitPatches":
                    print("-" * 40)
                    print("Orbit patches:")
                    print()
                    for index in range(len(value)):
                        print("Patch {}:".format(index))
                        for a, b in sorted(value[index].items()):
                            print("{}: {}".format(a, b))
                        print()

                    print("-" * 40)
                else:
                    print("{}: {}".format(key, value))

class Verb99(ExtendedVerb):

 

    def __init__(self, **kwargs):



        self.object_requesting_proceed = kwargs["object_requesting_proceed"]
        super().__init__(name="Please enable engine", verb_number="99")

    def execute(self):


        if self.dsky.current_verb:
            self.dsky.current_verb.terminate()
        super().execute()


        self.dsky.blank_all_registers()

        Verb.computer.dsky.set_register("99", "verb")
        self.dsky.request_data(requesting_object=self.object_requesting_proceed, display_location=None,
                             is_proceed_available=True)


verbs = OrderedDict()
clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
for class_tuple in clsmembers:
    if class_tuple[0][-1].isdigit():
        verbs[class_tuple[0][-2:]] = class_tuple[1]