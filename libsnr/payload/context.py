"""
Context management utilities. Some snr functions require a context variable to work, functions in this module help creating a context for a payload
"""

import os as _os
from libsnr.util.programs.mount import Mount as _Mount
from libsnr.util.programs.mount import PIPE as _PIPE


def create_context_for_mountpoint(mountpoint: str):
    """
     @brief Create context for mount point
     @param mountpoint Path to mount point.
     @return dict Generated context
     @return None If context creation fails
    """
    context = {
        "temp_dir": mountpoint,
        "is_device": True
    }
    mount = _Mount(stdout=_PIPE)
    mount.invoke_and_wait(None)
    mtab_raw_data = mount.stdout.read().decode()
    for line in mtab_raw_data.splitlines():
        source, _, dest, __ = line.split(maxsplit=3)
        if dest == mountpoint:
            context["device"] = source
            break
    else:
        return None
    context["part_prefix"] = ""
    if _os.path.basename(context["device"]).startswith(("nvme", "loop")):
        context["part_prefix"] = "p"
    return context
