from warg import NOD

from heimdallr.utilities.nvidia.packing import get_nv_info


def pull_gpu_info(include_graphics_processes: bool = True) -> dict:
    """Get all information about all your graphics cards.

    Returns:
      dict: The returned result is a dict with 3 keys: count, driver_version and devices:
          count: Number of gpus found
          driver_version: The version of the system’s graphics driver
          devices: It's a list and every item is a namedtuple Device which has 10 fields, for exzample id,
          name and fan_speed etc.
                   It should be noted that the Process field is also a namedtuple which has 11 fields."""

    driver_version, devices = get_nv_info(include_graphics_processes)

    info = NOD()

    info["count"] = len(devices)
    info["driver_version"] = driver_version
    info["devices"] = devices
    return info.as_dict()
