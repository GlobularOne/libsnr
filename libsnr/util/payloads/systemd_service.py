"""
Module containing a class providing systemd service file support
"""

from libsnr.util.payloads.systemd_unit import SystemdSectionType, SystemdUnit as _SystemdUnit


class SystemdService(_SystemdUnit,
                     suffix=".service",
                     extra_sections=("Service",)):
    """
     @brief Class providing systemd service file support
    """
    Service_section: SystemdSectionType = {}
