"""
Module containing a class providing systemd target file support
"""

from libsnr.util.payloads.systemd_unit import SystemdUnit as _SystemdUnit


class SystemdTarget(_SystemdUnit, suffix=".target", extra_sections=()):
    """
     @brief Class providing systemd target file support
    """
