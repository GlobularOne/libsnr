"""
Format the partitions on the target
"""
from libsnr.payload_generation.common import clean_and_exit as _clean_and_exit
from libsnr.util.common_utils import print_debug as _print_debug
from libsnr.util.program_wrapper import PIPE as _PIPE
from libsnr.util.program_wrapper import STDOUT as _STDOUT
from libsnr.util.program_wrapper import ProgramWrapper as _ProgramWrapper


def format_target(context):
    """
     @brief Format partitions on the target
     @param context Context dictionary 
     @return True if successful
     @return False if not successful
    """
    _print_debug("Formatting partitions")
    for index, tool, flags in (
        ("2", "mkfs.vfat", ("-F32",)),
        ("3", "mkfs.ext4", ("-F", "-L", "Rootfs"))
    ):
        part = f"{context['device_name']}{context['part_prefix']}{index}"
        errorcode = _ProgramWrapper(tool, stdout=_PIPE, stderr=_STDOUT).invoke_and_wait(None,
                                                                                        *flags,
                                                                                        part)
        if errorcode != 0:
            return _clean_and_exit(context, "Formatting failed", True)
    return True
