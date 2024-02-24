"""
Common utilities for payload generation
"""
import os as _os
import shutil as _shutil

from libsnr.util.common_utils import print_debug as _print_debug
from libsnr.util.common_utils import print_error as _print_error
from libsnr.util.program_wrapper import ProgramWrapper as _ProgramWrapper, DEVNULL as _DEVNULL
from libsnr.util.programs.mount import Mount as _Mount
from libsnr.util.programs.umount import Umount as _Umount


def bind_required_rootfs_dirs(context):
    """
     @brief Bind rootfs directories that are required for a chroot environment
     @param context Context dictionary 
    """
    for node in ("dev", "proc", "sys"):
        _print_debug(f"Binding /{node}")
        dest = _os.path.join(context["temp_dir"], node)
        _Mount().invoke_and_wait(None, "-B", f"/{node}", dest)


def unbind_required_rootfs_dirs(context: dict):
    """
     @brief Unbind required rootfs dirs.
     @param context Context dictionary
    """
    if "temp_dir" in context:
        for node in ("dev", "proc", "sys", "boot/efi"):
            _print_debug(f"Unmounting /{node}")
            dest = _os.path.join(context["temp_dir"], node)
            _Umount().invoke_and_wait(None, dest, options={"q": None})


def clean_on_success(context: dict, unmount_loop=False, clear_tempdir=False):
    """
     @brief Clean up after success.
     @param context Context dictionary
     @param unmount_loop Whether or not to unmount the loop device
     @param clear_tempdir Whether or not to clear temp dir
     @return True always returns True
    """
    unbind_required_rootfs_dirs(context)
    if clear_tempdir and "temp_dir" in context:
        _Umount().invoke_and_wait(
            None, context["temp_dir"], options={"q": None})
        _shutil.rmtree(context["temp_dir"])
    if not context["is_device"] and unmount_loop:
        _ProgramWrapper("losetup", stdout=_DEVNULL, stderr=_DEVNULL).invoke_and_wait(None,
                                                                                     options={"detach": context["device_name"]})
    if "temp_dir" in context:
        _shutil.rmtree(context["temp_dir"], ignore_errors=True)
    return True


def clean_and_exit(context, message, unmount_loop=False, clear_tempdir=False):
    """
     @brief Clean and exit with error
     @param context Context dictionary 
     @param message error message to pass to clean_on_success
     @param unmount_loop if True unmount the loop
     @param clear_tempdir if True clear the temporary directory
     @return False always return False
    """
    _print_error(message)
    clean_on_success(context, unmount_loop, clear_tempdir)
    return False
