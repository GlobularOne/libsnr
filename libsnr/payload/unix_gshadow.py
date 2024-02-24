"""
Module containing a class offering a clean interface to gshadow entries and a few utility functions
"""
import os as _os
import copy as _copy


class UnixGShadowEntry:
    """
     @brief Class offering a clean interface to gshadow entries
    """
    group_name: str
    password: str
    administrators: list
    members: list
    locked: bool

    def __init__(self, group_name: str, password: str,
                 administrators: list, members: list,
                 locked: bool):
        self.group_name = group_name
        self.password = password
        self.administrators = _copy.deepcopy(administrators)
        self.members = _copy.deepcopy(members)
        self.locked = locked

    def __str__(self):
        locked_str = ""
        if self.locked:
            locked_str = "!"
        return f"{self.group_name}:{locked_str}{self.password}:{','.join(self.administrators)}:{','.join(self.members)}"


def parse_unix_gshadow_line(line: str) -> UnixGShadowEntry:
    """
     @brief Parse a gshadow line and return a UnixGShadowEntry
     @param line The line to parse.
     @return UnixGShadowEntry The parsed UnixPasswdEntry
    """
    group_name, password, administrators_raw, members_raw = line.split(":", 4)
    administrators = ",".split(administrators_raw)
    members = ",".split(members_raw)
    locked = False
    if password.startswith("!"):
        password = password[1:]
        locked = True
    return UnixGShadowEntry(group_name, password, administrators, members, locked)


def parse_unix_gshadow_file(root: str = "/"):
    """
     @brief Parse the gshadow file and return list of gshadow objects
     @param root root of the directory to look for gshadow file
     @return list[UnixGShadowEntry] list of gshadow objects
    """
    gshadow_file = _os.path.join(root, "etc", "gshadow")
    gshadows = []
    with open(gshadow_file, encoding="utf-8") as stream:
        for line in stream.readlines():
            if len(line.strip()) != 0:
                try:
                    gshadows.append(parse_unix_gshadow_line(line))
                except Exception:  # pylint: disable=broad-exception-caught
                    pass
    return gshadows


def format_unix_gshadow_line(gshadow: UnixGShadowEntry):
    """
     @brief Format a UnixGShadowEntry for use in /etc/gshadow.
     @param gshadow The UnixGShadowEntry to format.
     @return str The formatted string representation of the UnixGShadowEntry
    """
    return str(gshadow)


def format_unix_gshadow_file(gshadows: list):
    """
     @brief Format a list of gshadow objects for use in /etc/shadow.
     @param gshadows list of gshadows to format
     @return str string with formatted gshadow file
    """
    output = ""
    for passwd in gshadows:
        output += str(passwd) + "\n"
    return output
