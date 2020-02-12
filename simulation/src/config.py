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
import os
from collections import OrderedDict

DEBUG = False
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROGRAM_NAME = "Atlas"
VERSION = "1.0.0"
LICENCE_FILE = os.path.join(BASE_DIR, "licence")
IMAGES_DIR = os.path.join(BASE_DIR, "assets/")
IP = "127.0.0.1"
PORT = "8085"
URL = "http://" + IP + ":" + PORT + "/telemachus/datalink?"
DISPLAY_UPDATE_INTERVAL = 500
COMP_ACTY_FLASH_DURATION = 100
LOOP_TIMER_INTERVAL = 50
SLOW_LOOP_TIMER_INTERVAL = 2000
ENABLE_COMP_ACTY_FLASH = True
LOG_LEVELS = [
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
]
current_log_level = "INFO"
DIRECTIONS = [
    "prograde",
    "retrograde",
    "normalplus",
    "normalminus",
    "radialplus",
    "radialminus",
    "node",
]
TELEMACHUS_BODY_IDS = {
    "Kerbol": "0",
    "Kerbin": "1",
    "Mun": "2",
    "Minmus": "3",
    "Moho": "4",
    "Eve": "5",
    "Duna": "6",
    "Ike": "7",
    "Jool": "8",
    "Laythe": "9",
    "Vall": "10",
    "Bop": "11",
    "Tylo": "12",
    "Gilly": "13",
    "Pol": "14",
    "Dres": "15",
    "Eeloo": "16",
}
_UNSORTED_ALARM_CODES = {
    110: "Error contacting KSP",
    111: "Telemetry not available",
    115: "No burn data loaded",
    116: "Program doesn't exist",
    120: "No phase angle data available",
    223: "Invalid target selected",
    224: "Orbit not circular",
    225: "Vessel and target orbits inclination too far apart",
    226: "Time of ignition less than 2 minutes in the future",
    310: "Program hasn't been finished yet, watch this space :)",
    410: "Autopilot error",
    501: "Uplink file does not exist, aborting uplink",
}
ALARM_CODES = OrderedDict(sorted(_UNSORTED_ALARM_CODES.items()))
OCTAL_BODY_IDS = {}
for key, value in TELEMACHUS_BODY_IDS.items():
    value = oct(int(value))
    value = value[2:]
    OCTAL_BODY_IDS[value] = key
OCTAL_BODY_NAMES = {value: key for key, value in OCTAL_BODY_IDS.items()}
PROGRAM_DESCRIPTION = "This is a reimplementation Apollo Guidance Computer (AGC) for Project Atlas."
with open(LICENCE_FILE) as f:
    LICENCE = f.readlines()
LICENCE = "".join(LICENCE)
SHORT_LICENCE = "Saturn X is under the MIT License, which means you can redistribute it free of any charge."

COPYRIGHT = "(C) 2019 Firebolt, Inc. & Firebolt Space Agency"
WEBSITE = "https://bitbucket.org/aaronhma/atlas/"
DEVELOPERS = "Firebolt, Inc. & Firebolt Space Agency"
ICON = os.path.join(BASE_DIR, "icon.png")