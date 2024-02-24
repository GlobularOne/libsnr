"""
Add the finishing touch to the target rootfs
"""
import json as _json
import os as _os

from libsnr.util.chroot_program_wrapper import \
    ChrootProgramWrapper as _ChrootProgramWrapper
from libsnr.util.common_utils import print_debug as _print_debug
from libsnr.util.program_wrapper import PIPE as _PIPE
from libsnr.util.program_wrapper import STDOUT as _STDOUT
from libsnr.util.program_wrapper import ProgramWrapper as _ProgramWrapper
from libsnr.payload_generation.common import \
    bind_required_rootfs_dirs as _bind_required_rootfs_dirs
from libsnr.payload_generation.common import clean_and_exit as _clean_and_exit

FSTAB_FORMAT = """\
# Snr-generated fstab
# <file system>  <mount point>  <type>  <options>          <dump>  <pass>
UUID={root_uuid} /              ext4    errors=remount-ro  0       1
UUID={esp_uuid}  /boot/efi      vfat    umask=0077         0       0
"""


def finish_target(context: dict):
    """
     @brief Add the finishing touch to the target rootfs
     @param context Context dictionary 
     @return True if successful
     @return False if not successful
    """
    _print_debug("Adding the finishing touch to the target")
    _bind_required_rootfs_dirs(context)
    lsblk = _ProgramWrapper("lsblk", stdout=_PIPE)
    errorcode = lsblk.invoke_and_wait(None, context["device_name"], options={
                                      "J": None, "o": "NAME,UUID"})
    if errorcode != 0:
        return _clean_and_exit(context, "Discovering partition UUIDs failed", True, True)
    parts_info = _json.load(lsblk.stdout)["blockdevices"][0]["children"]
    esp_part_name = _os.path.basename(
        context["device_name"]) + context["part_prefix"] + "2"
    root_part_name = _os.path.basename(
        context["device_name"]) + context["part_prefix"] + "3"
    esp_uuid = None
    root_uuid = None
    for part_info in parts_info:
        if part_info["name"] == esp_part_name:
            esp_uuid = part_info["uuid"]
        if part_info["name"] == root_part_name:
            root_uuid = part_info["uuid"]
    if esp_uuid is None:
        return _clean_and_exit(context, "ESP UUID not found!", True, True)
    if root_uuid is None:
        return _clean_and_exit(context, "Rootfs UUID not found!", True, True)
    with open(_os.path.join(context["temp_dir"], "etc", "fstab"), "w", encoding="ascii") as stream:
        stream.write(FSTAB_FORMAT.format(
            esp_uuid=esp_uuid, root_uuid=root_uuid))
    _print_debug("Generating initramfs")
    errorcode = _ChrootProgramWrapper(context, "update-initramfs", stdout=_PIPE, stderr=_STDOUT).invoke_and_wait(None, options={
        "c": None, "k": "all",
    })
    if errorcode != 0:
        return _clean_and_exit(context, "Generating initramfs failed", True, True)
    _print_debug("Updating grub configuration")
    with open(_os.path.join(context["temp_dir"], "etc", "default", "grub"),
              encoding="ascii") as stream:
        grub_cfg = stream.read()
        grub_cfg = grub_cfg.replace("GRUB_TIMEOUT=5", "GRUB_TIMEOUT=0")
        grub_cfg = grub_cfg.replace(
            "#GRUB_DISABLE_RECOVERY=\"true\"", "GRUB_DISABLE_RECOVERY=\"true\"")
    with open(_os.path.join(context["temp_dir"], "etc", "default", "grub"), "w",
              encoding="ascii") as stream:
        stream.write(grub_cfg)
    errorcode = _ChrootProgramWrapper(
        context, "update-grub", stdout=_PIPE, stderr=_STDOUT).invoke_and_wait(None)
    if errorcode != 0:
        return _clean_and_exit(context, "Updating grub configuration failed")
    _print_debug("Clearing root password")
    errorcode = _ChrootProgramWrapper(context, "passwd").invoke_and_wait(None,
                                                                         "root", options={"d": None, "q": None})
    if errorcode != 0:
        return _clean_and_exit(context, "Clearing root password failed")
    return True
