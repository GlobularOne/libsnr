"""
Library support for the safety pin. The safety pin is a feature on all payloads.
It checks whatever the payload is installed or not and if not running from a target, it won't run.
All the payloads that come with snr do use the safety pin.
For custom written payloads, you must use require_lack_of_safety_pin at the very
start of your payload. To ensure your payload doesn't run in the host accidentally.
"""
import os as _os


def check_lack_of_safety_pin():
    """
     @brief Check if the safety pin is lacking
     @return True if there is a problem False
    """
    return _os.path.exists("root/.give_em_hell")


def remove_safety_pin(root: str):
    """
     @brief Remove the safety pin 
     @param root path to root of
    """
    with open(_os.path.join(root, "root", ".give_em_hell"), "w") as stream:
        stream.write("Safety Pin")


def require_lack_of_safety_pin():
    """
     @brief Check if we lack the safety pin. If the safety pin exists, exit the program
    """
    if not check_lack_of_safety_pin():
        raise SystemExit(1)
