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
import logging
import time

from src import config
if config.DEBUG:
    from pudb import set_trace

LOG_VIEWER = None

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%d/%m/%y %H:%M',
                    filename='../logs/guidance.log',
                    filemode='a')

gc_log = logging.getLogger()


def seconds_to_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return {
        "days": days,
        "hours": hours,
        "minutes": minutes,
        "seconds": round(seconds, 2),
    }


def log(message="", log_level="DEBUG"):
    if log_level not in config.LOG_LEVELS:
        gc_log.error("Log level does not exist!")
        return
    now = time.strftime("%d/%m/%Y %H:%M:%S")

    if log_level == "DEBUG":
        gc_log.debug(message)
    elif log_level == "INFO":
        gc_log.info(message)
    elif log_level == "WARNING":
        gc_log.warning(message)
    elif log_level == "ERROR":
        gc_log.error(message)
    elif log_level == "CRITICAL":
        gc_log.critical(message)
    print("{:20}{:10}{}".format(now, log_level, message))
