"""
Module containing a ProgramWrapper sub-class wrapping mount tool
"""
from libsnr.util.program_wrapper import ProgramWrapper as _ProgramWrapper
# pylint: disable=unused-import
from libsnr.util.program_wrapper import PIPE, STDOUT, DEVNULL


class Mount(_ProgramWrapper):
    """
    @brief ProgramWrapper sub-class wrapping mount tool
    """

    def __init__(self, *args, stdin=None,
                 stdout=None, stderr=None, command_verb: None | str = None,
                 options: dict[str, str] | None = None, cwd: None | str = None):
        super().__init__(*args, "mount", stdin=stdin, stdout=stdout, stderr=stderr,
                         command_verb=command_verb, options=options, cwd=cwd)
