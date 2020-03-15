# 🎖 @TODO(aaronhma): Step 1: import everything
from . import config
from . import camera
from . import service_worker
from .spec import * as spec
from .trajectory import * as tj
from .rocket_control import * as rc
from .rocket_manuevers import * as rm

# 🎖 @TODO(aaronhma): Step 2: Declare everything
ram = [] # Memory storage

# 🎖 @TODO(aaronhma): Step 3: Enable camera
camera.camera(mirror_status=True)

# 🎖 @TODO(aaronhma): Step 4: Setup
spec.bit_test.test()

# @TODO(aaronhma): Step 5: Calc trajectory
tj.__TODO__

# @TODO(aaronhma): Step 6: Fire rockets
rc.__TODO__

# @TODO(aaronhma): Step 7: Alpha
rc.__TODO__

# @TODO(aaronhma): Step 8: Burnout
rc.__TODO__

# @TODO(aaronhma): Step 9: Disable 2nd stage
rm.__TODO__

# @TODO(aaronhma): Step 10: Remove 2nd stage
rm.__TODO__

# 🎖 @TODO(aaronhma): Step 11: Delete 2nd stage RAM
del ram