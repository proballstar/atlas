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
