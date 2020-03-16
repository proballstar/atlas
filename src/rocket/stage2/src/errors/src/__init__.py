from . import OtherError as err
from . import MemoryOverload as ram_err
from . import SensoryOverload as sensor_err

# @TODO(aaronhma): Setup
err.init()
ram_err.init()
sensor_err.init()

err.catchErrors()
ram_err.catchErrors()
sensor_err.catchErrors()