"""
Install GRUB for both UEFI and BIOS boot on the target
"""
import os as _os

from libsnr.util.chroot_program_wrapper import \
    ChrootProgramWrapper as _ChrootProgramWrapper
from libsnr.util.common_utils import print_debug as _print_debug
from libsnr.util.chroot_program_wrapper import PIPE as _PIPE
from libsnr.util.chroot_program_wrapper import STDOUT as _STDOUT
from libsnr.util.programs.mount import Mount as _Mount
from libsnr.payload_generation.common import \
    bind_required_rootfs_dirs as _bind_required_rootfs_dirs
from libsnr.payload_generation.common import clean_and_exit as _clean_and_exit
from libsnr.payload_generation.common import \
    unbind_required_rootfs_dirs as _unbind_required_rootfs_dirs


def install_grub(context: dict):
    """
     @brief Install GRUB for both UEFI and BIOS boot on the target
     @param context Context dictionary 
     @return True if successful
     @return False if not successful
    """
    BOOT_MOUNT_INFO = (
        (f"{context['device_name']}{context['part_prefix']}2", "boot/efi"),
    )
    for src, dest in BOOT_MOUNT_INFO:
        _print_debug(f"Mounting /{dest}")
        _os.makedirs(_os.path.join(context["temp_dir"], dest))
        errorcode = _Mount().invoke_and_wait(None,
                                             src,
                                             _os.path.join(context['temp_dir'], dest))
        if errorcode != 0:
            return _clean_and_exit(context, "Preparing to install grub failed", True, True)
    _bind_required_rootfs_dirs(context)
    _print_debug("Installing UEFI grub")
    errorcode = _ChrootProgramWrapper(context, "grub-install", stdout=_PIPE, stderr=_STDOUT).invoke_and_wait(None,
                                                                                                             context['device_name'],
                                                                                                             options={"uefi-secure-boot": None,
                                                                                                                      "removable": None})
    if errorcode != 0:
        return _clean_and_exit(context, "Installing grub failed", True, True)
    _print_debug("Install BIOS grub")
    errorcode = _ChrootProgramWrapper(context, "grub-install", stdout=_PIPE, stderr=_STDOUT).invoke_and_wait(None,
                                                                                                             context['device_name'],
                                                                                                             options={"target": "i386-pc"})
    if errorcode != 0:
        return _clean_and_exit(context, "Installing grub failed", True, True)
    _unbind_required_rootfs_dirs(context)
    return True
