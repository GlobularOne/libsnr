"""
Module containing a class offering a clean interface to passwd entries and a few utility functions
"""
import os as _os

# If a passwd entry's password field equals this, the password is stored in /etc/shadow
SHADOW_PASSWORD = "x"


class UnixPasswdEntry:
    """
     @brief Class offering a clean interface to shadow entries
    """
    login_name: str
    password: str
    uid: int
    gid: int
    comment: str
    home: str
    shell: str
    locked: bool

    def __init__(self, login_name: str, password: str,
                 uid: int, gid: int, comment: str,
                 home: str, shell: str, locked: bool):
        self.login_name = login_name
        self.password = password
        self.uid = uid
        self.gid = gid
        self.comment = comment
        self.home = home
        self.shell = shell
        self.locked = locked

    def __str__(self):
        locked_str = ""
        if self.locked:
            locked_str = "!"
        return f"{self.login_name}:{locked_str}{self.password}:{self.uid}:{self.gid}:{self.comment}:{self.home}:{self.shell}"

    def is_password_stored_in_shadow(self):
        return self.password == SHADOW_PASSWORD


def parse_unix_passwd_line(line: str) -> UnixPasswdEntry:
    """
     @brief Parse a passwd line and return a UnixPasswdEntry
     @param line The line to parse.
     @return UnixPasswdEntry The parsed UnixPasswdEntry
    """
    login_name, password, uid, gid, comment, home, shell = line.split(":", 7)
    locked = False
    if password.startswith("!"):
        password = password[1:]
        locked = True
    if len(shell) == 0:
        shell = "/bin/sh"
    return UnixPasswdEntry(login_name, password, int(uid), int(gid), comment, home, shell, locked)


def parse_unix_passwd_file(root: str = "/"):
    """
     @brief Parse the passwd file and return list of passwd objects
     @param root root of the directory to look for passwd file
     @return list[UnixPasswdEntry] list of passwd objects
    """
    passwd_file = _os.path.join(root, "etc", "passwd")
    passwds = []
    with open(passwd_file, encoding="utf-8") as stream:
        for line in stream.readlines():
            if len(line.strip()) != 0:
                # One line we can't parse shouldn't make the whole thing go down
                try:
                    passwds.append(parse_unix_passwd_line(line))
                except Exception:  # pylint: disable=broad-exception-caught
                    pass
    return passwds


def format_unix_passwd_line(passwd: UnixPasswdEntry):
    """
     @brief Format a UnixPasswdEntry for use in /etc/passwd.
     @param passwd The UnixPasswdEntry to format.
     @return str The formatted string representation of the UnixPasswdEntry
    """
    return str(passwd)


def format_unix_passwd_file(passwds: list):
    """
     @brief Format a list of passwd objects for use in /etc/shadow.
     @param passwds list of passwds to format
     @return str string with formatted passwd file
    """
    output = ""
    for passwd in passwds:
        output += str(passwd) + "\n"
    return output
