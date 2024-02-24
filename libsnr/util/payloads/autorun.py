"""
Module containing a class providing support for automatically running executables on boot while preserving order
"""
import os as _os

from libsnr.util.payloads.systemd_service import SystemdService as _SystemdService
from libsnr.util.payloads.systemd_target import SystemdTarget as _SystemdTarget
from libsnr.util.program_wrapper import ProgramWrapper as _ProgramWrapper
from libsnr.util.payloads.systemd_unit import \
    SYSTEMD_SYSTEM_PATH as _SYSTEMD_SYSTEM_PATH
from libsnr.util.common_utils import print_debug as _print_debug
from pprint import pformat as _pformat

class Autorun:
    """
     @brief Class providing support for automatically running executables on boot while preserving order
    """
    _services: list[_SystemdService] = []
    _custom_target: _SystemdTarget
    _context: dict

    def __init__(self, context: dict):
        _print_debug("Autorun instance created")
        snr_target = _SystemdTarget(context, "snr")
        snr_target.Unit_section["Description"] = "Snr boot target"
        snr_target.Unit_section["Requires"] = "multi-user.target"
        snr_target.Unit_section["After"] = "multi-user.target"
        self._custom_target = snr_target
        self._context = context

    def add_executable(self, path: str, name: str| None = None):
        """
         @brief Add an executable to be executed to the systemd configuration
         @param path Path to the executable
         @param name Name of the service
        """
        service = _SystemdService(self._context, _os.path.basename(path.split(" ", maxsplit=1)[0]) if name is None else name)
        service.Unit_section["Description"] = f"Autorun service for {path}"
        service.Service_section["ExecStart"] = path
        service.Service_section["Type"] = "simple"
        service.Service_section["ExecRestart"] = "/usr/bin/true"
        service.Service_section["ExecStop"] = "/usr/bin/true"
        service.Service_section["StandardInput"] = "tty"
        service.Service_section["StandardOutput"] = "tty"
        service.Service_section["TTYPath"] = "/dev/tty1"
        service.Install_section["RequiredBy"] = "snr.target"
        if len(self._services) > 1:
            _print_debug(
                f"Service is to be executed after {self._services[-1].basename}")
            # Preserve the original order
            service.Service_section["After"] = self._services[-1].basename
            service.Service_section["Requires"] = self._services[-1].basename
        if _os.path.exists(_os.path.join(self._context["temp_dir"], path)):
            errorcode = _ProgramWrapper("chmod").invoke_and_wait(None, "+x", _os.path.join(self._context["temp_dir"], path))
            if errorcode != 0:
                _print_debug("Marking service executable as +x failed")
        else:
            _print_debug("Skipping making service executable as +x due to the executable not existing")
        self._services.append(service)
        _print_debug(
            f"New service added:\nUnit: {_pformat(service.Unit_section)}\nService: {_pformat(service.Service_section)}\nInstall:{_pformat(service.Install_section)}")

    def write(self):
        """
         @brief Write the systemd configuration to the target
        """
        target_requires = "".join(
            [service.basename for service in self._services])
        # Update the Requires entry of snr.target
        self._custom_target.Unit_section["Requires"] = target_requires
        # Create the snr target and link it as the default one
        self._custom_target.write()
        try:
            _os.remove(_os.path.join(_SYSTEMD_SYSTEM_PATH(
                self._context), "default.target"))
        except FileNotFoundError:
            pass
        _os.symlink("snr.target", _os.path.join(_SYSTEMD_SYSTEM_PATH(self._context),
                                                "default.target"))
        snr_target_requires_dir = _os.path.join(_SYSTEMD_SYSTEM_PATH(self._context),
                                                "snr.target.requires")
        for service in self._services:
            service.write(False, False)
            _os.symlink(_os.path.join("..", service.basename),
                        _os.path.join(snr_target_requires_dir,
                                      service.basename))
