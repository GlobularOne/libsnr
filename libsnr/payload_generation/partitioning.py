"""
Partition the target device
"""
import os as _os
import time as _time

from libsnr.util.common_utils import print_debug as _print_debug
from libsnr.util.program_wrapper import PIPE as _PIPE
from libsnr.util.program_wrapper import STDOUT as _STDOUT
from libsnr.util.program_wrapper import ProgramWrapper as _ProgramWrapper
from libsnr.payload_generation.common import clean_and_exit as _clean_and_exit


def partition_target(context: dict):
    """
     @brief Create partitions on the block device
     @param context Context dictionary 
     @return True if successful
     @return False if not successful
    """
    _print_debug("Partitioning target")
    _print_debug("Clearing partition data on disk")
    target = context["target"]
    errorcode = _ProgramWrapper(
        "sgdisk", stdout=_PIPE, stderr=_STDOUT).invoke_and_wait(None, "-z", target)
    if errorcode != 0:
        return _clean_and_exit(context, "Partitioning failed")
    _print_debug("Partitioning disk")
    sgdisk_options = {}
    for index, part_info in enumerate((
        ("+1M", "1:ef02", "BIOS Boot"),
        ("+128M", "2:ef00", "ESP"),
        ("-0", "3:8300", "Rootfs")
    )):
        size, typecode, name = part_info
        _print_debug(f"Creating a partition for {name}")
        sgdisk_options.clear()
        sgdisk_options["new"] = f"{index+1}::{size}"
        sgdisk_options["typecode"] = typecode
        sgdisk_options["change-name"] = name
        errorcode = _ProgramWrapper("sgdisk", stdout=_PIPE).invoke_and_wait(
            None, target, options=sgdisk_options)
        if errorcode != 0:
            return _clean_and_exit(context, "Partitioning failed")
    part_prefix = ""
    context["device_name"] = target
    if not context["is_device"]:
        _print_debug("Target is not a device, mounting it on loop")
        part_prefix = "p"
        # Setup a loop, we need proper partition access
        losetup = _ProgramWrapper("losetup", stdout=_PIPE)
        errorcode = losetup.invoke_and_wait(None, target,
                                            options={"find": None, "show": None})
        if errorcode != 0:
            return _clean_and_exit(context, "Partitioning failed")
        context["device_name"] = losetup.stdout.read().decode().strip()
    elif context["device_name"].startswith("nvme"):
        part_prefix = "p"
    _print_debug("Probing partitions")
    errorcode = _ProgramWrapper("partprobe").invoke_and_wait(
        None, context["device_name"])
    if errorcode != 0:
        return _clean_and_exit(context, "Partitioning failed", True)
    _print_debug("Giving kernel time to discover the partitions")
    _time.sleep(1)
    _print_debug("Checking if all partitions exist")
    for i in range(1, 4):
        if not _os.path.exists(f"{context['device_name']}{part_prefix}{i}"):
            _print_debug(
                f"Partition {i} not found! ({context['device_name']}{part_prefix}{i})")
            return _clean_and_exit(context, "Partitioning failed", True)
    context["part_prefix"] = part_prefix
    return True
