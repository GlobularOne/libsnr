"""
Module for receiving the machine architecture generally and for a few packages
"""
import platform as _platform

from libsnr.core import options as _options


def get_arch():
    """
     @brief Get the machine's architecture or if set (has priority) the architecture the user selected
    """
    if hasattr(_options, "arch"):
        return _options.arch
    machine = _platform.machine()
    if machine in ("i386", "i486", "i586", "i686"):
        return "i386"
    return machine


def get_kernel_arch():
    """
     @brief Get the architecture in a way that \c linux-image-{get_kernel_arch()} is an existing debian package
    """
    # Output of uname -i and uname -o is unknown in many situations
    # (Which also makes platform.processor unreliable)
    # So translate them based on architecture
    arch = get_arch()
    if arch == "x86_64":
        return "amd64"
    return arch


def get_grub_arch():
    """
    Get the architecture in a way that grub-efi-{get_grub_arch()}
    is an existing debian package
    """
    arch = get_kernel_arch()
    if arch == "i386":
        return "ia32"
    return arch
