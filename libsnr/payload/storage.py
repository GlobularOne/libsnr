"""
Utility functions to help with the storage.
Allows working with LVM and getting information on all and any disk or partition
"""
import json as _json
import copy as _copy
from libsnr.util.program_wrapper import ProgramWrapper as _ProgramWrapper
from libsnr.util.program_wrapper import PIPE as _PIPE


###############################################################################
# Block and partition support
###############################################################################

def query_all_block_info() -> list:
    """
     @brief Query block information for all block devices.
     @return list A list of block devices
    """
    lsblk = _ProgramWrapper("lsblk", stdout=_PIPE)
    lsblk.invoke_and_wait(None,  options={
                          "J": None, "M": None, "b": None, "o": "NAME,UUID,TYPE,SIZE,PATH"})
    blockdevices = _json.load(lsblk.stdout)
    return blockdevices["blockdevices"]


def query_all_partitions(block_info: list | None = None):
    """
     @brief Query all partitions in block_info
     @param block_info list of block info queried or if None it will be queried
     @return list list of partition paths
    """
    if block_info is None:
        block_info = query_all_block_info()
    partitions = []
    for v in block_info:
        if "children" in v:
            for child in v["children"]:
                if child["type"] == "part":
                    partitions.append(child["path"])
    return partitions


def query_partition_info_by_path(path: str, block_info: list | None = None):
    """
     @brief Query block info for a partition.
     @param path Path to the partition.
     @param block_info list of block info queried or if None it will be queried
     @return dict A dict with information about the partition
    """
    if block_info is None:
        block_info = query_all_block_info()
    for v in block_info:
        if "children" in v:
            for child in v["children"]:
                if child["type"] == "part" and child["path"] == path:
                    return _copy.deepcopy(child)


def query_partition_info_by_uuid(uuid: str, block_info: list | None = None):
    """
     @brief Query block info for partition with uuid
     @param uuid uuid of partition to query
     @param block_info list of block info queried or if None it will be queried
     @return dict Partition info
     @return None If query failed
    """
    if block_info is None:
        block_info = query_all_block_info()
    for v in block_info:
        if "children" in v:
            for child in v["children"]:
                if child["type"] == "part" and child["uuid"] == uuid:
                    return _copy.deepcopy(child)


def query_partition_info_by_name(name: str, block_info: list | None = None):
    """
     @brief Query block info for partition with given name
     @param name Name of partition to query
     @param block_info list of block info queried or if None it will be queried
     @return dict Partition info
     @return None If query failed
    """
    if block_info is None:
        block_info = query_all_block_info()
    for v in block_info:
        if "children" in v:
            for child in v["children"]:
                if child["type"] == "part" and child["name"] == name:
                    return _copy.deepcopy(child)

###############################################################################
# LVM support
###############################################################################


def lvm_scan_all():
    """
     @brief Scans disks for LVM LVs
    """
    _ProgramWrapper("vgscan").invoke_and_wait(None, options={
                                                   "q": None, "y": None})
    _ProgramWrapper("lvscan").invoke_and_wait(None, options={
        "q": None, "y": None})


def lvm_activate_all_vgs():
    """
     @brief Activate all VGs
    """
    _ProgramWrapper("pvchange").invoke_and_wait(None, options={
                                                   "q": None, "y": None, "a": "y"})


###############################################################################
# Misc
###############################################################################


def get_partition_root(partition: str, block_info: list | None = None):
    """
     @brief Get the root path of a partition
     @param partition partition to look for.
     @param block_info list of block info queried or if None it will be queried
     @return str Root path
     @return None if partition is not present in \c block_info
    """
    if block_info is None:
        block_info = query_all_block_info()
    for block in block_info:
        if partition.startswith(block["path"]):
            return block["path"]
    else:
        # We cannot continue
        return None
