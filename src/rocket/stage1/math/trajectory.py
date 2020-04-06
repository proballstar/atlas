#
# MIT License
#
# Copyright (c) 2017 - 2020 Firebolt Space Agency,
# Copyright (c) 2017 - 2020 Firebolt, Inc,
# Copyright (C) 2020 - Present Aaron Ma,
# Copyright (c) 2020 - Present Rohan Fernandes.
# All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# @TODO(aaronhma): Create trajectory variables
import tensorflow as tf
from .common import format_helpers
from .common import format

TRAJECTORY = (0x60)
DESTINATION = "Moon" # choose from moon, mars, etc.
TRAJECTORY_X = tf.random.uniform((1,50))
TRAJECTORY_Y = tf.random.uniform((1,50))
TRAJECTORY_Z = tf.random.uniform((1,50))

# @TODO(aaronhma): put all the trajectory and destinations into file: trajectory.txt

# @TODO(aaronhma): destroy all useless variables with ```del``` to save RAM
del TRAJECTORY
del DESTINATION
del TRAJECTORY_X
del TRAJECTORY_Y
del TRAJECTORY_Z

# @TODO(aaronhma): add a formal ending
print(format.print_(format_helpers.sep()))
