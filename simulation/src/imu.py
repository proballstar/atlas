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
from src.telemachus import check_connection, get_telemetry
from src import utils, config
if config.DEBUG:
    from pudb import set_trace


class IMU:
    def __init__(self, computer):

        self.computer = computer
        self._is_on = False
        self.is_course_aligned = False
        self.is_fine_aligned = False
        self.gyro_angles = {
            "inner": 0.0,
            "middle": 0.0,
            "outer": 0.0,
        }

    def on(self):
        if check_connection() == False:
            utils.log("Cannot connect to KSP", "WARNING")
        else:
            self.set_coarse_align()

    def update_gyro_angles(self):

        self.gyro_angles["inner"] = get_telemetry("pitch")
        self.gyro_angles["middle"] = get_telemetry("heading")
        self.gyro_angles["outer"] = get_telemetry("roll")

    def check_for_gimbal_lock(self):
        if self.is_fine_aligned:
            if (70 <= self.gyro_angles["middle"] <= 85) or \
                (95 <= self.gyro_angles["middle"] <= 110) or \
                (250 <= self.gyro_angles["middle"] <= 265) or \
                    (275 <= self.gyro_angles["middle"] <= 290):
                self.computer.dsky.set_annunciator("gimbal_lock")
            else:
                if (85 < self.gyro_angles["middle"] < 95) or \
                        (265 < self.gyro_angles["middle"] <= 275):
                    self.set_coarse_align()

    def set_coarse_align(self):
        self.is_fine_aligned = False
        self.is_course_aligned = True
        self.computer.dsky.set_annunciator("no_att")
        if self.update_gyro_angles in self.computer.main_loop_table:
            self.computer.main_loop_table.remove(self.update_gyro_angles)
        if self.check_for_gimbal_lock in self.computer.main_loop_table:
            self.computer.main_loop_table.remove(self.check_for_gimbal_lock)
        utils.log("IMU coarse align set")

    def set_fine_align(self):
        if check_connection() == False:
            utils.log(
                "IMU: cannot complete fine align, no connection to KSP", log_level="ERROR")
            return
        self.is_fine_aligned = True
        self.is_course_aligned = False
        self.computer.dsky.set_annunciator("gimbal_lock", False)
        self.computer.dsky.set_annunciator("no_att", False)
        utils.log("IMU fine align set")
