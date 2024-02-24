"""
Satisfy the reported payload dependencies
"""
from libsnr.core import options as _options
from libsnr.payload_generation.common import \
    bind_required_rootfs_dirs as _bind_required_rootfs_dirs
from libsnr.payload_generation.common import clean_and_exit as _clean_and_exit
from libsnr.payload_generation.common import \
    unbind_required_rootfs_dirs as _unbind_requires_rootfs_dirs
from libsnr.util.chroot_program_wrapper import \
    ChrootProgramWrapper as _ChrootProgramWrapper
from libsnr.util.common_utils import print_debug as _print_debug


def satisfy_dependencies(context: dict):
    """
     @brief Install dependencies of the payload
     @param context the context to be used for installing
     @return True if successful
     @return False if not successful
    """
    if hasattr(_options.payload_module, "DEPENDENCIES") and len(_options.payload_module.DEPENDENCIES) != 0:
        _bind_required_rootfs_dirs(context)
        _print_debug(
            f"Installing dependencies of the payload: {' '.join(_options.payload_module.DEPENDENCIES)}")
        errorcode = _ChrootProgramWrapper(context, "apt-get").invoke_and_wait(None, *_options.payload_module.DEPENDENCIES, options={
            "quiet": "2"
        })
        if errorcode != 0:
            return _clean_and_exit(context, "Installing dependencies of payload failed")
        _unbind_requires_rootfs_dirs(context)
    else:
        _print_debug("Payload has no dependencies, nothing to do")
    return True
