#  Copyright (c) 2021. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.


import sys
from .system_resources import *

if sys.platform[:3] == "win":
    from .windows_task_scheduler_utilities import *
else:
    pass
    # TODO: USE DRAUGR FOR NOW; make wrapper for platform agnostic behaviour later
    # from draugr.os_utilities.linux_utilities.systemd_utilities import *

    # from .systemd_utilities import * # deprecated
