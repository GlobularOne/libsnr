"""
Module containing a ProgramWrapper sub-class wrapping umount tool
"""
# pylint: disable=unused-import
from libsnr.util.program_wrapper import DEVNULL, PIPE, STDOUT
from libsnr.util.program_wrapper import ProgramWrapper as _ProgramWrapper


class Umount(_ProgramWrapper):
    """
    @brief ProgramWrapper sub-class wrapping umount tool
    """

    def __init__(self, *args, stdin=None,
                 stdout=None, stderr=None, command_verb: None | str = None,
                 options: dict[str, str] | None = None, cwd: None | str = None):
        super().__init__(*args, "umount", stdin=stdin, stdout=stdout, stderr=stderr,
                         command_verb=command_verb, options=options, cwd=cwd)
