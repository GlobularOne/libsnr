"""
Module containing utility functions to install libsnr onto the target
"""
import os as _os
import shutil as _shutil
from libsnr.util.common_utils import print_debug as _print_debug

## Path to the currently installed libsnr's root
LIBSNR_DIR = _os.path.dirname(_os.path.dirname(_os.path.dirname(__file__)))


def DIST_PACKAGES_DIR(context: dict):
    """
     @brief Return the path to the dist-packages directory
     @param context The context to use for obtaining the directory
     @return str The path to the dist-packages
    """
    return _os.path.join(context["temp_dir"], "lib", "python3", "dist-packages")


def install_libsnr(context: dict):
    """
     @brief Install libsnr onto target.
     @param context context to install libsnr
    """
    _print_debug("Installing libsnr to target")
    _os.makedirs(DIST_PACKAGES_DIR(context), exist_ok=True)
    _shutil.copytree(LIBSNR_DIR, _os.path.join(DIST_PACKAGES_DIR(context), "libsnr"))
    _print_debug("Installed libsnr successfully")
