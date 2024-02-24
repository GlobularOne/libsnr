"""
Module containing a class wrapping a program to be executed inside a chroot environment
"""

from libsnr.util.program_wrapper import ProgramWrapper as _ProgramWrapper
# pylint: disable=unused-import
from libsnr.util.program_wrapper import PIPE, STDOUT, DEVNULL


class ChrootProgramWrapper(_ProgramWrapper,
                           interpreter=("chroot",
                                        None)):
    """
    @brief Class wrapping a program to be executed inside a chroot environment
    """

    def __init__(self, context: dict,
                 program: str, *args, stdin=None,
                 stdout=None, stderr=None,
                 command_verb: None | str = None,
                 options: dict[str, str] | None = None,
                 cwd: None | str = None):
        super().__init__(program, *args, stdin=stdin, stdout=stdout, stderr=stderr,
                         command_verb=command_verb, options=options, cwd=cwd)
        self._interpreter = (self._interpreter[0], context["temp_dir"])
