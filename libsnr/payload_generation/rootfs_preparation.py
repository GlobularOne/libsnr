"""
Prepare rootfs for payload generation
"""
import shutil as _shutil
import tempfile as _tempfile

from libsnr.core import common_paths as _common_paths
from libsnr.core import options as _options
from libsnr.util.common_utils import print_debug as _print_debug
from libsnr.util.common_utils import print_info as _print_info
from libsnr.util.common_utils import rootfs_open as _rootfs_open
from libsnr.util.programs.mount import Mount as _Mount
from libsnr.payload_generation.common import clean_and_exit as _clean_and_exit


def prepare_rootfs(context: dict):
    """
     @brief Prepare rootfs for payload generation.
     @param context Context dictionary
     @return True if successful
     @return False if not successful
    """
    _print_info("Preparing for payload generation")
    _print_debug("Unpacking rootfs image")
    context["temp_dir"] = _tempfile.mkdtemp(prefix="snr")
    errorcode = _Mount().invoke_and_wait(
        None, f"{context['device_name']}{context['part_prefix']}3", context["temp_dir"])
    if errorcode != 0:
        _print_debug("Mounting rootfs failed")
        return _clean_and_exit(context, "Copying rootfs to target failed", True)
    _print_debug("Copying rootfs")
    try:
        _shutil.unpack_archive(_common_paths.ROOTFS_ARCHIVE_PATH,
                               context["temp_dir"],
                               _common_paths.ROOTFS_ARCHIVE_FORMAT)
    except Exception as exc:  # pylint: disable=broad-exception-caught
        return _clean_and_exit(context, f"Unpacking rootfs image failed ({exc})")
    _print_debug("Preparing rootfs")
    _print_debug("Writing hostname")
    with _rootfs_open(context, "etc/hostname", "w") as stream:
        stream.write(_options.DEFAULT_HOSTNAME + "\n")
    _print_debug("Writing dns configuration")
    with _rootfs_open(context, "etc/resolv.conf", "w") as stream:
        stream.write(f"nameserver {_options.DEFAULT_PRIMARY_DNS}\n"
                     f"nameserver {_options.DEFAULT_SECONDARY_DNS}\n"
                     )
    return True
