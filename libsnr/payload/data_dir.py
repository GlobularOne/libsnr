"""
/data directory support
"""
import os as _os

from libsnr.util.programs.mount import Mount as _Mount


def fix_data_dir():
    """
     @brief Ensure a writable /data directory. If the rootfs is mounted writable, it does nothing. Otherwise it mounts a temporary in-ram filesystem on /data
    """
    try:
        _os.mkdir("/data/_fix_data_dir_test")
    except Exception:
        _Mount().invoke_and_wait(None, "tmpfs",
                                 "/data", options={"t": "tmpfs"})
    else:
        _os.rmdir("/data/_fix_data_dir_test")


def data_open(file, mode="r", buffering: int = -1, encoding: str | None = None):
    """
     @brief Open a file in read - only mode.
     @param file The name of the file to open.
     @param mode The mode to open the file in.
     @param buffering The buffering size in bytes.
     @param encoding The encoding to use.
     @return file-like object
    """
    stream = open(_os.path.join("/data", file), mode, buffering, encoding)

    def __enter__():
        return stream.__enter__()

    def __exit__(exc_type, exc_val, exc_tb):
        return stream.__exit__(exc_type, exc_val, exc_tb)
    return stream


def data_mkdir(path: str, mode: int = 511):
    """
     @brief Create a directory if it doesn't exist
     @param path Path to the directory to create
     @param mode Permissions to set for the directory
    """
    _os.mkdir(path, mode=mode)
