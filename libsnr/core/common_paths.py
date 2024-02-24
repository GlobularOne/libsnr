"""
Module containing common paths used by snr and possibly by payloads
"""
import os as _os

## User's home path
USER_HOME_PATH = _os.path.expanduser("~")

## Snr's configuration path
CONFIG_PATH = _os.path.join(USER_HOME_PATH, ".config", "snr")

## Snr's cache path
CACHE_PATH = _os.path.join(USER_HOME_PATH, ".cache", "snr")

## Snr's rootfs archive base path
ROOTFS_ARCHIVE_BASE_PATH = _os.path.join(CACHE_PATH, "stable-{machine}")
## Snr's rootfs archive path
ROOTFS_ARCHIVE_PATH = ""
## Snr's rootfs archive format
ROOTFS_ARCHIVE_FORMAT = "gztar"
## Snr's rootfs archive file extension
ROOTFS_ARCHIVE_EXTENSION = ".tar.gz"


def format_rootfs_archive_path(machine: str):
    """
     @brief Format the ROOTFS_ARCHIVE_*_PATH variables
     @param machine Chosen machine architecture
    """
    global ROOTFS_ARCHIVE_BASE_PATH  # pylint: disable=global-statement
    global ROOTFS_ARCHIVE_PATH  # pylint: disable=global-statement
    ROOTFS_ARCHIVE_BASE_PATH = ROOTFS_ARCHIVE_BASE_PATH.format(machine=machine)
    ROOTFS_ARCHIVE_PATH = ROOTFS_ARCHIVE_BASE_PATH + ROOTFS_ARCHIVE_EXTENSION
