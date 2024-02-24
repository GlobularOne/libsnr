"""
Module containing a class offering a clean interface to group entries and a few utility functions
"""
import os as _os
import copy as _copy


class UnixGroupEntry:
    """
     @brief Class offering a clean interface to group entries
    """
    group_name: str
    password: str
    gid: int
    user_list: list

    def __init__(self, group_name: str, password: str,
                 gid: int, user_list: list):
        self.group_name = group_name
        self.password = password
        self.gid = gid
        self.user_list = _copy.deepcopy(user_list)

    def __str__(self):
        return f"{self.group_name}:{self.password}:{self.gid}:{','.join(self.user_list)}"


def parse_unix_group_line(line: str) -> UnixGroupEntry:
    """
     @brief Parse a group line and return a UnixGroupEntry
     @param line The line to parse.
     @return UnixGroupEntry The parsed UnixGroupEntry
    """
    group_name, password, gid, user_list_raw = line.split(":", 4)
    user_list = user_list_raw.split(",")
    return UnixGroupEntry(group_name, password, int(gid), user_list)


def parse_unix_group_file(root: str = "/"):
    """
     @brief Parse the group file and return list of group objects
     @param root root of the directory to look for group file
     @return list[UnixGroupEntry] list of group objects
    """
    group_file = _os.path.join(root, "etc", "group")
    groups = []
    with open(group_file, encoding="utf-8") as stream:
        for line in stream.readlines():
            if len(line.strip()) != 0:
                # One line we can't parse shouldn't make the whole thing go down
                try:
                    groups.append(parse_unix_group_line(line))
                except Exception:  # pylint: disable=broad-exception-caught
                    pass
    return groups


def format_unix_group_line(group: UnixGroupEntry):
    """
     @brief Format a UnixGroupEntry for use in /etc/group.
     @param group The UnixGroupEntry to format.
     @return str The formatted string representation of the UnixGroupEntry
    """
    return str(group)


def format_unix_group_file(groups: list):
    """
     @brief Format a list of group objects for use in /etc/shadow.
     @param groups list of groups to format
     @return str string with formatted group file
    """
    output = ""
    for group in groups:
        output += str(group) + "\n"
    return output
