"""
Module containing utility functions to organize writing to screen
"""
import sys as _sys

from libsnr.core import options as _options

## System message symbol
SYS = "-->"
## Debug message symbol
DEBUG = f"[\033[35m.\033[39m]"
## Informational message symbol
INFO = f"[\033[34m!\033[39m]"
## Successful message symbol
OK = f"[\033[32m+\033[39m]"
## Warning message symbol
WARNING = f"[\033[33m*\033[39m]"
## Error message symbol
ERROR = f"[\033[31m-\033[39m]"


def carriage_return():
    """
     @brief Return to the previous line
    """
    _sys.stdout.write('\r')


def clear_screen():
    """
     @brief Clears the screen
    """
    print("\033[2J")


def print_sys(*args, sep=' ', end='\n', file=None, flush=False):
    """
     @brief Print system message to stdout
     @param sep Separator between values
     @param end Ending character ('\\n')
     @param file File to print to (default sys.stdout)
     @param flush Flag to flush output
    """
    print(SYS, *args, sep=sep, end=end, file=file, flush=flush)


def print_debug(*args, sep=' ', end='\n', file=None, flush=False):
    """
     @brief Print debug message to stdout if verbose mode is on
     @param sep Separator between values
     @param end Ending character ('\\n')
     @param file File to print to (default sys.stdout)
     @param flush Flag to flush output
    """
    if _options.verbose:
        print(DEBUG, *args, sep=sep, end=end, file=file, flush=flush)


def print_info(*args, sep=' ', end='\n', file=None, flush=False):
    """
     @brief Print informational message to stdout if quiet mode is off
     @param sep Separator between values
     @param end Ending character ('\\n')
     @param file File to print to (default sys.stdout)
     @param flush Flag to flush output
    """
    if not _options.quiet:
        print(INFO, *args, sep=sep, end=end, file=file, flush=flush)


def print_ok(*args, sep=' ', end='\n', file=None, flush=False):
    """
     @brief Print a successful message to stdout
     @param sep Separator between values
     @param end Ending character ('\\n')
     @param file File to print to (default sys.stdout)
     @param flush Flag to flush output
    """
    print(OK, *args, sep=sep, end=end, file=file, flush=flush)


def print_warning(*args, sep=' ', end='\n', file=None, flush=False):
    """
     @brief Print a warning message to stdout
     @param sep Separator between values
     @param end Ending character ('\\n')
     @param file File to print to (default sys.stdout)
     @param flush Flag to flush output
    """
    print(WARNING, *args, sep=sep, end=end, file=file, flush=flush)


def print_error(*args, sep=' ', end='\n', file=None, flush=False):
    """
     @brief Print an error message to stdout
     @param sep Separator between values
     @param end Ending character ('\\n')
     @param file File to print to (default sys.stdout)
     @param flush Flag to flush output
    """
    print(ERROR, *args, sep=sep, end=end, file=file, flush=flush)


def print_fatal(*args, sep=' ', end='\n', file=None, flush=False):
    """
     @brief Print an error message to stdout and exit
     @param sep Separator between values
     @param end Ending character ('\\n')
     @param file File to print to (default sys.stdout)
     @param flush Flag to flush output
    """
    print(ERROR, *args, sep=sep, end=end, file=file, flush=flush)
    _sys.exit(_options.default_exit_code)
