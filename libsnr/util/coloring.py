"""
Snr terminal colors support
"""
import sys as _sys

## ANSI CSI
CSI = "\033["

## ANSI foreground color black
BLACK = CSI + "30m"
## ANSI foreground color red
RED = CSI + "31m"
## ANSI foreground color green
GREEN = CSI + "32m"
## ANSI foreground color yellow
YELLOW = CSI + "33m"
## ANSI foreground color blue
BLUE = CSI + "34m"
## ANSI foreground color magenta
MAGENTA = CSI + "35m"
## ANSI foreground color cyan
CYAN = CSI + "36m"
## ANSI foreground color white
WHITE = CSI + "37m"
## ANSI foreground color reset
RESET = CSI + "39m"


def fore_reset():
    """
     @brief Change terminal's foreground color to the initial
    """
    _sys.stdout.write(RESET)


def fore_red():
    """
     @brief Change terminal's foreground color to the red
    """
    _sys.stdout.write(RED)


def fore_blue():
    """
     @brief Change terminal's foreground color to the blue
    """
    _sys.stdout.write(BLUE)


def fore_green():
    """
     @brief Change terminal's foreground color to the green
    """
    _sys.stdout.write(GREEN)


def fore_magenta():
    """
     @brief Change terminal's foreground color to the magenta
    """
    _sys.stdout.write(MAGENTA)
