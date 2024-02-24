"""
Snr core and common utilities. If a function is found here and also in libsnr.core, it is advised to use the one here
"""
import os as _os
import shutil as _shutil
import sys as _sys
import traceback as _traceback
# pylint: disable=unused-import
from shutil import get_terminal_size
# pylint: disable=unused-import
from libsnr.core import options as _options
# pylint: disable=unused-import
from libsnr.core.logging import (carriage_return, clear_screen, print_debug, print_error, print_fatal,
                                 print_info, print_ok, print_sys, print_warning)
# pylint: disable=unused-import
from libsnr.util.table import Table
# pylint: disable=unused-import
from libsnr.core import common_paths as _common_paths

EXTERNAL_CALL_FAILURE = "\x01"


def remake_dir(path: str):
    """
     @brief Remove and recreate a directory.
     @param path Path to the directory
    """
    _shutil.rmtree(path)
    _os.mkdir(path)


def graceful_exit():
    """
     @brief Gracefully exit the program
    """
    _sys.exit(_options.default_exit_code)


def call_external_function(func, *args, **kwargs):
    """
     @brief Call an external function catching and reporting any exceptions
     @param func Function to call. Must be a callable
     @return The return value of the called function, or if the call failed EXTERNAL_CALL_FAILURE
    """
    try:
        return func(*args, **kwargs)
    except Exception:  # pylint: disable=broad-exception-caught
        print_debug("Calling external function failed")
        print_debug("Stack:")
        print_debug("".join(_traceback.format_stack()))
        print_debug("Exception:")
        print_debug(_traceback.format_exc())
        return EXTERNAL_CALL_FAILURE


def rootfs_open(context: dict, file, mode="r", buffering: int = -1, encoding: str | None = None):
    """
     @brief Open a file in rootfs
     @param context A dictionary containing the test context
     @param file The file to open.
     @param mode The mode to open the file with
     @param buffering The buffering size to use
     @param encoding The encoding to use. If None the default encoding will be used
     @return file-like object Stream opened
    """
    stream = open(_os.path.join(
        context["temp_dir"], file), mode, buffering, encoding)

    def __enter__():
        return stream.__enter__()

    def __exit__(exc_type, exc_val, exc_tb):
        return stream.__exit__(exc_type, exc_val, exc_tb)
    return stream
