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


def charin(keypress, state, dsky, computer):

    def handle_control_register_load():

        if keypress.isalpha():
            computer.operator_error("Expecting numeric input")
            return

        display_register = state["display_location_to_load"]
        if state["register_index"] == 0:
            dsky.set_register(keypress, display_register, "1")

            state["input_data_buffer"] = keypress
            state["register_index"] += 1
        else:
            dsky.set_register(keypress, display_register, "2")
            state["register_index"] = 0
            state["input_data_buffer"] += keypress

    def handle_data_register_load():

        if keypress.isdigit() == False:
            utils.log("Expecting a digit for data load, got {}".format(
                keypress), log_level="ERROR")
            return
        display_register = state["display_location_to_load"]
        if state["register_index"] == 0:
            if keypress == "+":
                dsky.set_register("+", display_register)
            elif keypress == "-":
                dsky.set_register("-", display_register)
            else:
                dsky.set_register("b", display_register)
            state["register_index"] += 1
        if 1 <= state["register_index"] <= 5:
            dsky.set_register(keypress, display_register,
                              digit=state["register_index"])
            if state["register_index"] >= 5:
                state["register_index"] = 0
            else:
                state["register_index"] += 1
        state["input_data_buffer"] += keypress

    def handle_expected_data():

        if keypress == "P":
            dsky.verb_noun_flash_off()
            utils.log("Proceeding without input, calling {}".format(
                str(state["object_requesting_data"])))
            state["object_requesting_data"]("proceed")
            state["input_data_buffer"] = ""
            state["is_expecting_data"] = False
            return

        elif keypress == "E":
            input_data = state["input_data_buffer"]
            state["input_data_buffer"] = ""
            state["is_expecting_data"] = False
            dsky.verb_noun_flash_off()
            data_requester = state["object_requesting_data"]
            utils.log("Data load complete, calling {}({})".format(
                data_requester.__self__, data_requester.__name__))
            data_requester(input_data)

            return
        if state["display_location_to_load"] in ["verb", "noun", "program"]:
            handle_control_register_load()
        else:
            handle_data_register_load()

        if keypress.isalpha():

            computer.operator_error("Expecting numeric input")
            return

    def handle_verb_entry():

        if keypress == "C":
            state["verb_position"] = 0
            state["requested_verb"] = ""
            dsky.blank_register("verb")
            dsky.blank_register("noun")

            return

        if keypress == "N":
            state["is_verb_being_loaded"] = False
            state["is_noun_being_loaded"] = True
            state["verb_position"] = 0
        elif keypress == "E":
            state["is_verb_being_loaded"] = False
            state["verb_position"] = 0
        elif keypress.isalpha():
            computer.operator_error("Expected a number for verb choice")
            return
        elif state["verb_position"] == 0:
            dsky.set_register(value=keypress, register="verb", digit="1")
            state["requested_verb"] = keypress
            state["verb_position"] = 1
        elif state["verb_position"] == 1:
            dsky.set_register(value=keypress, register="verb", digit="2")
            state["requested_verb"] += keypress
            state["verb_position"] = 2

    def handle_noun_entry():

        if keypress == "C":
            state["noun_position"] = 0
            state["requested_noun"] = ""
            dsky.control_registers["noun"].digits[1].display("blank")
            dsky.control_registers["noun"].digits[2].display("blank")
            return

        if keypress == "N":
            state["is_noun_being_loaded"] = False
            state["is_verb_being_loaded"] = True
            state["noun_position"] = 0
        elif keypress == "E":
            state["is_noun_being_loaded"] = False
            state["noun_position"] = 0
        elif keypress.isalpha():
            computer.operator_error("Expected a number for noun choice")
            return
        elif state["noun_position"] == 0:
            dsky.set_register(keypress, "noun", digit="1")
            state["requested_noun"] = keypress
            state["noun_position"] = 1
        elif state["noun_position"] == 1:
            dsky.set_register(keypress, "noun", digit="2")
            state["requested_noun"] += keypress
            state["noun_position"] = 2

    def handle_entr_keypress():

        computer.execute_verb()
        state["requested_noun"] = ""

    def handle_reset_keypress():

        computer.reset_alarm_codes()
        dsky.reset_annunciators()
        if dsky.annunciators["opr_err"].blink_timer.isActive():
            dsky.annunciators["opr_err"].stop_blink()

    def handle_noun_keypress():

        state["is_verb_being_loaded"] = False
        state["is_noun_being_loaded"] = True
        state["requested_noun"] = ""
        dsky.blank_register("noun")

    def handle_verb_keypress():
        """ Handles VERB keypress
        :return: None
        """

        state["is_noun_being_loaded"] = False
        state["is_verb_being_loaded"] = True
        state["requested_verb"] = ""
        dsky.blank_register("verb")

    def handle_key_release_keypress():

        if state["backgrounded_update"]:
            backgrounded_update = state["backgrounded_update"].resume
            if state["display_lock"]:
                state["display_lock"].terminate()
            dsky.stop_annunciator_blink("key_rel")
            backgrounded_update()
            state["backgrounded_update"] = None
            state["is_verb_being_loaded"] = False
            state["is_noun_being_loaded"] = False
            state["is_data_being_loaded"] = False
            state["verb_position"] = 0
            state["noun_position"] = 0
            state["requested_verb"] = ""
            state["requested_noun"] = ""
            return

    if computer.is_powered_on == False:
        if keypress == "P":
            computer.on()
        else:
            utils.log("Key {} ignored because gc is off".format(keypress))
            return

    if state["is_expecting_data"]:
        handle_expected_data()
        return

    if keypress == "R":
        handle_reset_keypress()
        return

    if keypress == "K":
        handle_key_release_keypress()
        return

    if state["display_lock"]:
        state["display_lock"].background()

    if state["is_verb_being_loaded"]:
        handle_verb_entry()

    elif state["is_noun_being_loaded"]:
        handle_noun_entry()

    if keypress == "E":
        handle_entr_keypress()

    if keypress == "V":
        handle_verb_keypress()

    if keypress == "N":
        handle_noun_keypress()

    if keypress == "C":
        pass  # TODO
