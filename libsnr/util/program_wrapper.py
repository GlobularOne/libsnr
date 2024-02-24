"""
Module containing a class wrapping a program
"""
import os as _os
import shlex as _shlex
import shutil as _shutil
import subprocess as _subprocess

from libsnr.util.common_utils import print_debug as _print_debug

## Pass as either stdout, stderr or stdin and the stream becomes a usable pipe as a member with the same name
PIPE = _subprocess.PIPE
## Tie the stream to stdout
STDOUT = _subprocess.STDOUT
## Tie to stream to /dev/null
DEVNULL = _subprocess.DEVNULL


class ProgramWrapper:
    """
     @brief Class wrapping a program
    """
    ## Path of the program to execute
    path: str
    ## Working directory of the program
    cwd: None | str
    ## Command verb of the program (the first option passed on the command line, comes before \c args and \c options)
    command_verb: None | str
    ## Arguments to pass on the command line
    args: list[str]
    ## Options to pass on the command line
    options: dict[str, str | None]
    ## Executed program's stdin
    stdin = None
    ## Executed program's stdout
    stdout = None
    ## Executed program's stderr
    stderr = None
    _interpreter: tuple[str, str | None] = ("", None)
    _process: None | _subprocess.Popen
    _stdin = None
    _stdout = None
    _stderr = None

    def __init__(self,
                 program: str, *args, stdin=None,
                 stdout=None, stderr=None,
                 command_verb: None | str = None,
                 options: dict[str, str] | None = None,
                 cwd: None | str = None):
        if _os.path.isabs(program):
            self.path = program
        else:
            path = _shutil.which(program)
            if path is None:
                raise FileNotFoundError(f"Could not find program: '{program}'")
            self.path = path
        self.command_verb = command_verb
        self.args = [*args]
        if options is None:
            self.options = {}
        else:
            self.options = {**options}
        self.cwd = cwd
        self._process = None
        self._stdin = stdin
        self._stdout = stdout
        self._stderr = stderr

    def __init_subclass__(cls, interpreter: tuple[str, str | None] = ("", None)):
        cls._interpreter = interpreter

    def __repr__(self):
        return f"{type(self).__name__}("\
            f"{repr(self.path)}, {repr(self.args)}, "\
            f"command_verb={repr(self.command_verb)}, "\
            f"options={repr(self.options)}, cwd={repr(self.cwd)})"

    def set_command_verb(self, verb: str):
        """
         @brief Set the verb that will be used for command
         @param verb verb to be used for
        """
        self.command_verb = verb

    def add_arguments(self, *args, options: dict[str, str | None] | None = None):
        """
         @brief Add arguments to the command
         @param options dict of options to
        """
        self.args.extend(args)
        if options is not None:
            self.options = {**self.options, **options}

    def invoke(self, *args, options: dict[str, str | None] | None = None):
        """
         @brief Invoke the program with the given arguments
         @param options Options to pass to
        """
        # First ensure the program isn't already running
        if self._process is not None:
            if self._process.returncode is None:
                # Program is still running
                raise _subprocess.SubprocessError(
                    f"Program '{self.path}' is already running")
        self._process = None
        cwd = _os.getcwd() if self.cwd is None else self.cwd
        self.add_arguments(*args, options=options)
        cmdline = []
        if self._interpreter is None or self._interpreter[0] != "":
            cmdline.extend(self._interpreter)
        cmdline.append(self.path)
        if self.command_verb is not None:
            cmdline.append(_shlex.quote(self.command_verb))
        for option, value in self.options.items():
            if len(option) == 1:
                cmdline.append("-" + option)
            else:
                cmdline.append("--" + option)
            if value is not None:
                cmdline.append(_shlex.quote(value))
        cmdline.extend([_shlex.quote(arg) for arg in self.args])
        _print_debug(
            f"Executing program '{cmdline[0]}' with arguments: {cmdline[1:]}")
        self._process = _subprocess.Popen(cmdline, cwd=cwd, stdin=self._stdin,
                                          stdout=self._stdout, stderr=self._stderr)
        self.stdin = self._process.stdin
        self.stdout = self._process.stdout
        self.stderr = self._process.stderr

    def wait(self, timeout: float | None = None) -> int:
        """
         @brief Wait for the process to exit.
         @param timeout Time in seconds to wait for the process to exit.
         @return The exit code of the process
        """
        if self._process is None:
            raise _subprocess.SubprocessError("Program has never run")
        return self._process.wait(timeout)

    def invoke_and_wait(self, timeout: float | None, *args,
                        options: dict[str, str | None] | None = None) -> int:
        """
        @brief Invoke and wait for result.
        @param timeout Timeout in seconds. If None wait forever.
        @param options Options to pass to invoke.
        @return Number of seconds returned by wait
        """
        self.invoke(*args, options=options)
        return self.wait(timeout)
