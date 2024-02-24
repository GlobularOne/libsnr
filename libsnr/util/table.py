"""
Module containing a class allowing creation of tables to be printed with a clean interface
"""
from libsnr.util.coloring import RED as _RED, BLUE as _BLUE, RESET as _RESET
from libsnr.util.common_utils import get_terminal_size as _get_terminal_size


class Table:
    """
     @brief Class allowing creation of tables to be printed with a clean interface
    """
    # Header of the table
    header: str
    # Rows of the table, to be manipulated using the public functions
    rows: list[list[str]]

    def __init__(self, header: str, rows: list[list[str]] | None = None):
        self.header = header
        if rows is None or len(rows) == 0 or \
                (len(rows) == 1 and len(rows[0]) == 0):
            self.rows = [[]]
        else:
            self.rows = [*rows]

    def __repr__(self):
        """
         @brief Return the code representation of Table, exec(repr(t)) == t
        """
        return f"{type(self).__name__}({repr(self.header)}, {repr(self.rows)})"

    def _str_wrap(self, value: str, column_size: int):
        """
         @brief Wrap a string to fit a column
         @param value The string to wrap.
         @param column_size The size of the column.
         @return tuple[int, str] A tuple of the length of the string and the wrapped string
        """
        if not isinstance(value, str):
            raise ValueError("'value' is not a 'str'")
        if len(value) > column_size:
            if column_size <= 3:
                return column_size, "." * column_size
            return column_size, value[:column_size - 3] + "..."
        return len(value), value

    def _str_fit(self, value: str, column_size: int):
        """
         @brief Fits a string to a column
         @param value The string to fit in the column
         @param column_size The size of the column
         @return tuple[int, str] A tuple of the column size and
        """
        if not isinstance(value, str):
            raise ValueError("'value' is not a 'str'")
        if len(value) > column_size:
            if column_size <= 3:
                return column_size, "." * column_size
            return column_size, value[:column_size - 3] + "..."
        return column_size, value + " " * (column_size - len(value))

    def _format_row(self, row: list[str]):
        """
         @brief Formats a row of text to be displayed on the terminal.
         @param row The row to be formatted.
         @return str The formatted row as a str
        """
        output = "| "
        columns = _get_terminal_size().columns - 4
        red = True
        for value in row[:-1]:
            if columns == 0:
                output += " |"
                return output
            columns -= 3
            if columns <= 0:
                break
            length, line = self._str_wrap(value, columns)
            if red:
                color = _RED
                red = False
            else:
                color = _BLUE
                red = True
            output += color + line + _RESET + " | "
            columns -= length
        if red:
            color = _RED
        else:
            color = _BLUE
        length, line = self._str_fit(row[-1], columns)
        output += color + line + _RESET + " |\n"
        return output

    def __str__(self):
        output = self.header + "\n"
        output += "|" + (_get_terminal_size().columns-2) * "-" + "|\n"
        for row in self.rows:
            if len(row) != 0:
                line = self._format_row(row)
                output += line
                output += "|" + (_get_terminal_size().columns-2) * "-" + "|\n"
        return output

    def add_empty_row(self):
        """
         @brief Add an empty row to the table
        """
        self.rows.append([])

    def add_row(self, *args):
        """
         @brief Add a row to the table
        """
        self.rows.append([*args])

    def add_columns(self, *columns):
        """
         @brief Add columns to the end of the table
        """
        self.rows[-1].extend(columns)
