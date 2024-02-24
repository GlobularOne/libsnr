"""
Module that contains a class to format a string, replacing \@variable@ with value
"""


class AtFormatter:
    """
    @brief Class to format a string, replacing \@variable@ with value
    """
    variables: dict[str, str]

    def __init__(self, preset: dict[str, str] | None = None):
        if preset is not None:
            self.variables = dict(preset.items())

    def format_str(self, string: str):
        """
         @brief Formats a string according to the variables
         @param string The string to format.
         @return The formatted string with variables
        """
        for var, value in self.variables.items():
            if f"@{var}@" in string:
                string = string.replace(f"@{var}@", value)
        return string
