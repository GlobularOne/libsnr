"""
Module containing a class as a variable manager, containing methods to set, get and delete variables
"""
from dataclasses import dataclass as _dataclass
from warnings import warn as _warn

## Type that matches all possible variable types
VariableType = str | int | bool | list[str]
## Type of type that matches all possible variable types
VariableTypeType = type[str | int | bool | list[str]]
## Tuple that matches all possible variable types
VariableTypesTuple = (str, int, bool, list)


@_dataclass
class VariableInfo:  # pylint: disable=too-few-public-methods
    """
     @brief Dataclass containing a variable's info
    """
    description: str = ""
    length: int = -1
    var_type: VariableTypeType = str


class VariableManager:
    """
     @brief Class as a variable manager, containing methods to set, get and delete variables
    """
    _variables: dict[str, tuple[VariableType, VariableInfo]]
    _VariableValueType = tuple[VariableType, VariableInfo]

    def __init__(self,
                 pre: dict[str, _VariableValueType] | None = None):
        if pre is None:
            self._variables = {}
        else:
            self._variables = {**pre}

    def __repr__(self):
        return f"{type(self).__name__}({repr(self._variables)})"

    def has_variable(self, name: str):
        """
         @brief Check if variable is defined
         @param name Name of variable to check
         @return True if variable is defined False
        """
        return name in self._variables

    def set_variable(self, name: str, value: VariableType,
                     info_length: int = -1, info_description: str = ""):
        """
         @brief Set value of variable.
         @param name Name of variable to set
         @param value Value of variable
         @param info_length Length of variable if -1 no length will be set
         @param info_description Description of variable if
        """
        if isinstance(value, VariableTypesTuple):
            if isinstance(value, list):
                for i, element in enumerate(value):
                    if not isinstance(element, VariableTypesTuple):
                        raise ValueError(
                            f"Unsupported type of value[{i}]")
                value = list(value)
        else:
            raise ValueError(f"Unsupported type '{type(value)}'")

        if type(value) in (int, bool) and info_length != -1:
            _warn("Variables of integer types cannot have length")
            info_length = -1

        if name in self._variables:
            info = self._variables[name][1]
            if info.length != -1 and isinstance(value, (str, list)):
                if len(value) > info.length:
                    _warn(
                        f"Value does not fit the size ({info.length})")
                    info_length = -1
            if info_length != -1:
                info.length = info_length
            if len(info_description) == 0:
                info.description = info_description
        else:
            info = VariableInfo()
            info.length = info_length
            info.description = info_description
            info.var_type = type(value)
        self._variables[name] = (value, info)

    def del_variable(self, name: str):
        """
         @brief Delete a variable from the variable map
         @param name Name of the variable to
        """
        if name in self._variables:
            del self._variables[name]

    def get_variable(self, name: str) -> VariableType:
        """
         @brief Get the variable with the given name.
         @param name The name of the variable to get.
         @return The variable with the given name
        """
        if name in self._variables:
            return self._variables[name][0]
        raise ValueError(f"No variable named '{name}'")

    def get_variable_info(self, name: str) -> VariableInfo:
        """
         @brief Get information about a variable
         @param name Name of the variable to get information about
         @return VariableInfo Variable information
        """
        if name in self._variables:
            return self._variables[name][1]
        raise ValueError(f"No variable named '{name}'")

    def get_variables_name(self) -> list[str]:
        """
         @brief Get list of variables names.
         @return list[str] list of variable names
        """
        return list(self._variables.keys())

    def get_variables_value(self) -> list[VariableType]:
        """
         @brief Get list of variables values.
         @return list[VariableType] list of variable values
        """
        return list(v[0] for v in self._variables.values())

    def get_variables_info(self) -> list[VariableInfo]:
        """
         @brief Get list of all variable's info
         @return list[VariableInfo] list of all variable info
        """
        return list(v[1] for v in self._variables.values())
