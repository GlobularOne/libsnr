"""
Module containing a class offering a clean interface to shadow entries and a few utility functions
"""
import os as _os

# If a shadow entry's password field equals this, no password is required
PASSWORD_NO_LOGIN = "*"


class UnixShadowEntry:
    """
     @brief Class offering a clean interface to shadow entries
    """
    login_name: str
    password: str
    password_change_date: str
    min_password_age: str
    max_password_age: str
    password_warn_period: str
    password_inactivity_period: str
    expiration_date: str
    reserved: str
    locked: bool

    def __init__(self, login_name: str, password: str,
                 password_change_date: str, max_password_age: str,
                 min_password_age: str, password_warn_period: str,
                 password_inactivity_period: str, expiration_date: str,
                 reserved: str, locked: bool):
        self.login_name = login_name
        self.password = password
        self.password_change_date = password_change_date
        self.max_password_age = max_password_age
        self.min_password_age = min_password_age
        self.password_warn_period = password_warn_period
        self.password_inactivity_period = password_inactivity_period
        self.expiration_date = expiration_date
        self.reserved = reserved
        self.locked = locked

    def __str__(self):
        locked_str = ""
        if self.locked:
            locked_str = "!"
        return f"{self.login_name}:{locked_str}{self.password}:{self.password_change_date}:{self.max_password_age}:{self.min_password_age}:{self.password_warn_period}:{self.password_inactivity_period}:{self.expiration_date}:{self.reserved}"


def parse_unix_shadow_line(line: str) -> UnixShadowEntry:
    """
     @brief Parse a shadow line and return a UnixShadowEntry
     @param line The line to parse.
     @return UnixShadowEntry The parsed UnixShadowEntry
    """
    login_name, password, password_change_date, max_password_age, min_password_age, password_warn_period, password_inactivity_period, expiration_date, reserved = line.split(
        ":", 9)
    locked = False
    if password.startswith("!"):
        password = password[1:]
        locked = True
    return UnixShadowEntry(login_name, password, password_change_date, max_password_age, min_password_age, password_warn_period, password_inactivity_period, expiration_date, reserved, locked)


def parse_unix_shadow_file(root: str = "/"):
    """
     @brief Parse the shadow file and return list of shadow objects
     @param root root of the directory to look for shadow file
     @return list[UnixShadowEntry] list of shadow objects
    """
    shadow_file = _os.path.join(root, "etc", "shadow")
    shadows = []
    with open(shadow_file, encoding="utf-8") as stream:
        for line in stream.readlines():
            if len(line.strip()) != 0:
                try:
                    shadows.append(parse_unix_shadow_line(line))
                except Exception:  # pylint: disable=broad-exception-caught
                    pass
    return shadows


def format_unix_shadow_line(shadow: UnixShadowEntry):
    """
     @brief Format a UnixShadowEntry for use in /etc/shadow.
     @param shadow The UnixShadowEntry to format.
     @return str The formatted string representation of the UnixShadowEntry
    """
    return str(shadow)


def format_unix_shadow_file(shadows: list):
    """
     @brief Format a list of shadow objects for use in /etc/shadow.
     @param shadows list of shadows to format
     @return str string with formatted shadow file
    """
    output = ""
    for shadow in shadows:
        output += str(shadow) + "\n"
    return output
