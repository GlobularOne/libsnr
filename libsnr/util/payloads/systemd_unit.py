"""
Module containing a class providing a more clean interface to work with systemd unit files
"""
import configparser as _configparser
import os as _os
from warnings import warn as _warn
from libsnr.util.common_utils import print_debug as _print_debug
from pprint import pformat as _pformat


def SYSTEMD_SYSTEM_PATH(context: dict):
    """
     @brief Return the path to systemd's system directory
     @param context A dictionary containing the following keys : temp_dir - The path to the temporary directory used.
     @return str The path to systemd's system directory
    """
    return _os.path.join(context["temp_dir"], "usr", "lib", "systemd", "system")


_ValidOptionValueType = str | int | bool
## Type for a system section
SystemdSectionType = dict[str, _ValidOptionValueType]


class _SystemdConfigParser(_configparser.ConfigParser):
    def optionxform(self, optionstr: str) -> str:
        return optionstr


class SystemdConfigFileBase:
    """
     @brief Class providing basic systemd unit file parsing, is not usually used directly.
    """
    _base_sections: tuple[str, ...] = ()
    _extra_sections: tuple[str, ...] = ()
    root: str = ""
    path: str = ""
    suffix: str = ""
    basename: str = ""

    def __init_subclass__(cls, root: str, base_sections=()):
        cls.root = root
        cls._base_sections = tuple(base_sections)

    def read(self):
        """
         @brief Read and parse configuration file
        """
        parser = _SystemdConfigParser()
        if len(parser.read(self.path)) != 1:
            raise FileNotFoundError(
                f"No such file or directory: {self.path}")
        section_names = parser.sections()
        for section_name in section_names:
            section_name = section_name.replace("-", "_")
            if section_name in self._extra_sections or section_name in self._base_sections:
                setattr(self, f"{section_name}_section",
                        {**parser[section_name]})
            else:
                _warn(
                    f"SystemdUnit: Unrecognized section '{section_name}'")

    def _write(self):
        """
         @brief Write the unit file
        """
        sections = {}
        for section_name in self._base_sections:
            sections[section_name.replace(
                "_", "-")] = getattr(self, f"{section_name}_section")
        for section_name in self._extra_sections:
            sections[section_name.replace(
                "_", "-")] = getattr(self, f"{section_name}_section")
        _print_debug(
            f"Writing unit file {self.basename} with data:\n{_pformat(sections)}")
        parser = _SystemdConfigParser()
        parser.read_dict(sections)
        with open(self.path, "w", encoding="utf-8") as stream:
            parser.write(stream, False)

    def write(self):
        """
         @brief Write unit the file
        """
        self._write()


class SystemdUnit(SystemdConfigFileBase,
                  root="/nonexistent",
                  base_sections=("Unit", "Install")):
    """
    @brief Class providing a more clean interface to work with systemd unit files
    """
    Unit_section: SystemdSectionType = {}
    Install_section: SystemdSectionType = {}
    _context: dict

    def __init__(self, context: dict, name: str):
        for extra_section in self._extra_sections:
            setattr(self, f"{extra_section}_section", dict())
        for base_section in self._base_sections:
            setattr(self, f"{base_section}_section", dict())
        self.root = SYSTEMD_SYSTEM_PATH(context)
        self.path = _os.path.join(self.root, name + self.suffix)
        self.basename = _os.path.basename(self.path)
        self._context = context

    def __init_subclass__(cls, suffix: str, extra_sections=()):
        cls.suffix = suffix
        cls._extra_sections = tuple(extra_sections)

    def write(self, make_wants_dir=True, make_requires_dir=True):
        """
         @brief Write the config to disk.
         @param make_wants_dir Whether or not to make the .wants directory.
         @param make_requires_dir Whether or not to make the .requires directory
        """
        self._write()
        if make_wants_dir:
            _os.mkdir(_os.path.join(self.root, self.basename) + ".wants")
        if make_requires_dir:
            _os.mkdir(_os.path.join(self.root, self.basename) + ".requires")
