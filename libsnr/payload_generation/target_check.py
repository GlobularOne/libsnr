"""
Check target to ensure it can host a snr-generated rootfs
"""
import fcntl as _fcntl
import os as _os
import stat as _stat
import struct as _struct

from libsnr.core import options as _options
from libsnr.util.common_utils import print_error as _print_error


def check_target(context: dict):
    """
     @brief Check the target and print error if it is not a file or block device or doesn't meet the size requirements
     @param context Context dictionary
     @return True if target is a file or a block device and meets the size requirements
     @return False if target is either not a file or a block device or does not meet the size requirements
    """
    target = context["target"]
    if _os.path.isfile(target):
        # Use os.path.getsize to get the size
        context["output_size"] = _os.path.getsize(target)
        context["is_device"] = False
    elif _stat.S_ISBLK(_os.stat(target).st_mode):
        # Use ioctl to get the size
        buffer = b'\0' * 8
        with open(target, "rb") as stream:
            _fcntl.ioctl(stream.fileno(), 0x80081272, buffer)
        context["output_size"] = _struct.unpack("L", buffer)[0]
        context["is_device"] = True
    else:
        _print_error(f"'{target}' is not a file neither a device")
        return False
    if context["output_size"] < _options.MINIMUM_TARGET_SIZE:
        _print_error(
            f"'{target}' is not at least {_options.MINIMUM_TARGET_SIZE / 1024 / 1024}MBs")
        return False
    return True
