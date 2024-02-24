"""
Module for user-passed options and shared variables
"""
import types as _types

## Whatever snr is run in verbose mode or not
verbose: bool = False

## Whatever or not snr is run in quiet mode
quiet: bool = False

## Whatever or not snr is run in interactive mode
interactive: bool = True

## Whatever or not snr is initializing
initializing: bool = False

## Snr's default exit code
default_exit_code: int = 1

## System architecture
arch: str

## Prompt when no payload is loaded
PROMPT_UNLOADED = "snr>"

## Format for the prompt when a payload is loaded
PROMPT_LOADED_FORMAT = "snr ({0})>"

## Prompt to use for input
prompt: str = PROMPT_UNLOADED

## Path to the currently loaded payload
payload_path: str = ""

## Python module of the loaded payload or None if no payload is loaded
payload_module: _types.ModuleType | None = None

## Minimum size all target mediums must at least be
MINIMUM_TARGET_SIZE = 1300 * 1024 * 1024

## Default hostname of generated images
DEFAULT_HOSTNAME = "snr"

## Default primary dns of generated images
DEFAULT_PRIMARY_DNS = "1.1.1.1"

## Default secondary dns of generated images
DEFAULT_SECONDARY_DNS = "1.0.0.1"
