from typing import Sequence
import sys
import os

if(os.name == 'nt'):
    import ctypes
    import msvcrt

    class _CursorInfo(ctypes.Structure):
        _fields_ = [
            ("size", ctypes.c_int),
            ("visible", ctypes.c_byte)
        ]

    _STD_OUTPUT_HANDLE = ctypes.windll.kernel32.GetStdHandle(-11)
else:
    import tty
    import termios

    _FILE_DESCRIPTOR = sys.stdin.fileno()
    _DEFAULT_TERMINAL_SETTING = termios.tcgetattr(_FILE_DESCRIPTOR)

class _Keys:
    SELECT = '\r'
    UP = {"nt": 'H', "posix": "\x1b[A"}
    DOWN = {"nt": 'P', "posix": "\x1b[B"}

_TERMINAL_HEIGHT = os.get_terminal_size().lines
_TERMINAL_WIDTH = os.get_terminal_size().columns

_DEFAULT_COLORS = ("default", "red", "green", "yellow", "blue", "magenta", "cyan", "white")

def _ansicolor(color: str | tuple[int, int, int]):
        if(type(color) is str):
            if(color.startswith("light")):
                return f"\033[9{_DEFAULT_COLORS.index(color.removeprefix('light_'))}m"
            else:
                return f"\033[3{_DEFAULT_COLORS.index(color)}m"
        else:
            return f"\033[38;2;{color[0]};{color[1]};{color[2]}m"

def _ansibgcolor(color: str | tuple[int, int, int]):
        if(type(color) is str):
            if(color.startswith("light")):
                return f"\033[10{_DEFAULT_COLORS.index(color.removeprefix('light_'))}m"
            else:
                return f"\033[4{_DEFAULT_COLORS.index(color)}m"
        else:
            return f"\033[48;2;{color[0]};{color[1]};{color[2]}m"


def menu(
    title: str | Sequence[str],
    options: list[str] | tuple[str, ...],
    cursor_color: str | tuple[int, int, int],
    title_color: str | tuple[int, int, int] | Sequence[str | tuple[int, int, int] | None] | None = None,
    options_color: str | tuple[int, int, int] | Sequence[str | tuple[int, int, int] | None] | None = None,
    initial_cursor_position: int = 0,
) -> int:

    """Creates a pretty menu in console. Use arrow keys to move the cursor and enter key to select an option.
    Clears console once an option is selected and returns the index of the selected options.

    Args:
        - title: title of the menu, can be displayed on multiple lines if a list or a tuple is passed.
        - options: list of elements that can be selected by the user.
        - cursor_color: color of the cursor, available colors are `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`
        and their lighter versions (e.g. `light_red`), use custom color by providing a tuple containing color RGB values.
        - title_color (optional): color of the title, available colors are the same as `cursor_color`,
        customize the color of each line separately by providing a list of colors,
        each color will be associated with the line of the corresponding index (default color is terminal text color).
        - options_color (optional): color of options, available colors are the same as `cursor_color`,
        customize the color of every options separately by providing a list of colors,
        each color will be associated with the option of the corresponding index (default color is terminal text color).
        - initial_cursor_position (optional): index of the option where the initial cursor position is set (default position is first element).
    """

    if(not isinstance(title, Sequence)):
        raise TypeError(
            f"menu() argument 'title' expects str, list or tuple, not {type(title).__name__}"
        )
    elif(type(title) is not str and any(type(line) is not str for line in title)):
        raise TypeError(
            "all elements of menu() argument 'title' must be str"
        )

    if(type(options) not in (list, tuple)):
        raise TypeError(
            f"menu() argument 'options' expects list or tuple, not {type(options).__name__}"
        )
    elif(len(options) == 0):
        raise ValueError(
            "menu() argument 'options' cannot be empty"
        )
    elif(any(type(option) is not str for option in options)):
        raise TypeError(
            "all elements of menu() argument 'options' must be str"
        )

    if(type(title) is str and _TERMINAL_HEIGHT < len(options) + 4 or type(title) in (list, tuple) and _TERMINAL_HEIGHT < len(options) + len(title) + 2):
        raise RuntimeError(
           "terminal height is too low to display the menu, please resize your terminal"
        )

    vertical_spacing = (_TERMINAL_HEIGHT - len(options)) // 2

    if(type(cursor_color) not in (str, tuple)):
        raise TypeError(
            f"menu() argument 'cursor_color' expects str or tuple, not {type(cursor_color).__name__}"
        )
    elif(type(cursor_color) is tuple):
        if(len(cursor_color) == 3 and all(type(value) is int and 0 <= value < 256 for value in cursor_color)):
            ansi_cursor_color = _ansibgcolor(cursor_color)
        else:
            raise ValueError(
                "menu() argument 'cursor_color' has invalid RGB values"
            )
    elif(type(cursor_color) is str and cursor_color.removeprefix("light_") in _DEFAULT_COLORS):
        ansi_cursor_color = _ansibgcolor(cursor_color)
    else:
        raise ValueError(
            "menu() argument 'cursor_color' has an invalid color"
        )

    if(not isinstance(title_color, Sequence) and title_color is not None):
        raise TypeError(
            f"menu() argument 'title_color' expects str, list, tuple or None, not {type(title_color).__name__}"
        )
    elif(title_color is None):
        ansi_title_color = ""
        multiple_colors_for_title = False

    elif(type(title_color) is str and title_color.removeprefix("light_") in _DEFAULT_COLORS):
        multiple_colors_for_title = False
        ansi_title_color = _ansicolor(title_color)

    elif(type(title_color) is tuple and all(type(value) is int for value in title_color)):
        if(len(title_color) == 3 and all(0 <= value < 256 for value in title_color) ):
            multiple_colors_for_title = False
            ansi_title_color = _ansicolor(title_color)
        else:
            raise ValueError(
                "menu() argument 'title_color' has invalid RGB values"
            )
    elif(type(title_color) in (list, tuple)):
        if(all(((type(color) is str and color.removeprefix("light_") in _DEFAULT_COLORS)
                or (type(color) is tuple and len(color) == 3 and all(type(rgb_value) is int and 0 <= rgb_value < 256 for rgb_value in color))
                or color is None) for color in title_color)):

            if(len(title_color) <= len(title)):
                multiple_colors_for_title = True
                ansi_title_color = []

                for color in title_color:
                    if(color is None):
                        ansi_title_color.append("")
                    else:
                        ansi_title_color.append(_ansicolor(color))

                while(len(ansi_title_color) < len(title)):
                    ansi_title_color.append("")
            else:
                raise ValueError(
                    "menu() argument 'title_color' cannot have more colors than title has lines"
                )
        else:
            raise ValueError(
                "menu() argument 'title_color' has an invalid sequence of color"
            )
    else:
        raise ValueError(
            "menu() argument 'title_color' has an invalid color"
        )

    if(not isinstance(options_color, Sequence) and options_color is not None):
        raise TypeError(
            f"menu() argument 'options_color' expects str, list, tuple or None, not {type(options_color).__name__}"
        )
    elif(options_color is None):
        ansi_options_color = ""
        multiple_colors_for_options = False

    elif(type(options_color) is str and options_color.removeprefix("light_") in _DEFAULT_COLORS):
        multiple_colors_for_options = False
        ansi_options_color = _ansicolor(options_color)

    elif(type(options_color) is tuple and all(type(value) is int for value in options_color)):
        if(len(options_color) == 3 and all(0 <= value < 256 for value in options_color) ):
            multiple_colors_for_options = False
            ansi_options_color = _ansicolor(options_color)
        else:
            raise ValueError(
                "menu() argument 'options_color' has invalid RGB values"
            )
    elif(type(options_color) in (list, tuple)):
        if(all(((type(color) is str and color.removeprefix("light_") in _DEFAULT_COLORS)
                or (type(color) is tuple and len(color) == 3 and all(type(rgb_value) is int and 0 <= rgb_value < 256 for rgb_value in color))
                or color is None) for color in options_color)):

            if(len(options_color) <= len(options)):
                multiple_colors_for_options = True
                ansi_options_color = []

                for color in options_color:
                    if(color is None):
                        ansi_options_color.append("")
                    elif(type(color) is str):
                        ansi_options_color.append(_ansicolor(color))
                    else:
                        ansi_options_color.append(_ansicolor(color))

                while(len(ansi_options_color) < len(options)):
                    ansi_options_color.append("")
            else:
                raise ValueError(
                    "menu() argument 'options_color' cannot have more colors than options"
                )
        else:
            raise ValueError(
                "menu() argument 'options_color' has an invalid sequence of color"
            )
    else:
        raise ValueError(
            "menu() argument 'options_color' has an invalid color"
        )

    if(type(initial_cursor_position) is int):
        if(-len(options) <= initial_cursor_position < len(options)):
            cursor_height = vertical_spacing + options.index(options[initial_cursor_position])
        else:
            raise ValueError(
                f"'{initial_cursor_position}' is not an index of menu() argument 'options'"
                )
    elif(type(initial_cursor_position) is str):
        if(initial_cursor_position in options):
            cursor_height = vertical_spacing + options.index(initial_cursor_position)
        else:
            raise ValueError(
                f"'{initial_cursor_position}' is not an element of menu() argument 'options'"
            )
    else:
        raise TypeError(
            f"menu() argument 'initial_cursor_position' expects int or str, not {type(initial_cursor_position).__name__}"
        )

    if(os.name == 'nt'):
        cursor_info = _CursorInfo()
        ctypes.windll.kernel32.GetConsoleCursorInfo(_STD_OUTPUT_HANDLE, ctypes.byref(cursor_info))
        cursor_info.visible = False
        ctypes.windll.kernel32.SetConsoleCursorInfo(_STD_OUTPUT_HANDLE, ctypes.byref(cursor_info))

        os.system("cls")
    else:
        sys.stdout.write("\033[?25l")
        os.system("clear")

    if(type(title) is str):
        print('\n'*(vertical_spacing - 3))
        print(" " + ansi_title_color + title.center(_TERMINAL_WIDTH - 1) + '\n\n')
    else:
        print('\n'*(vertical_spacing - len(title) - 1))
        if(multiple_colors_for_title):
            for i, line in enumerate(title):
                print(" " + ansi_title_color[i] + line.center(_TERMINAL_WIDTH - 1))
        else:
            for line in title:
                print(" " + ansi_title_color + line.center(_TERMINAL_WIDTH - 1))
        sys.stdout.write('\n')

    key = None
    while(key != _Keys.SELECT):
        if(multiple_colors_for_options):
            for line, option in enumerate(options):
                if(line + vertical_spacing == cursor_height):
                    print(" " + ansi_cursor_color + ansi_options_color[line] + option.center(_TERMINAL_WIDTH - 1) + "\033[0m")
                else:
                    print(" " + ansi_options_color[line] + option.center(_TERMINAL_WIDTH - 1) + "\033[0m")
        else:
            for line, option in enumerate(options):
                if(line + vertical_spacing == cursor_height):
                    print(" " + ansi_cursor_color + ansi_options_color + option.center(_TERMINAL_WIDTH - 1) + "\033[0m")
                else:
                    print(" " + ansi_options_color + option.center(_TERMINAL_WIDTH - 1) + "\033[0m")

        if(os.name == 'nt'):
            key = msvcrt.getwch()
        else:
            tty.setraw(_FILE_DESCRIPTOR)
            key = sys.stdin.read(1)

            if(key == '\x1b'):
                char2 = sys.stdin.read(1)
                char3 = sys.stdin.read(1)

                key = key + char2 + char3

            termios.tcsetattr(_FILE_DESCRIPTOR, termios.TCSADRAIN, _DEFAULT_TERMINAL_SETTING)

        if(key == _Keys.UP[os.name]):
            if(cursor_height > vertical_spacing):
                cursor_height = cursor_height - 1
            else:
                cursor_height = vertical_spacing + len(options) - 1

        elif(key == _Keys.DOWN[os.name]):
            if(cursor_height < vertical_spacing + len(options) - 1):
                cursor_height = cursor_height + 1
            else:
                cursor_height = vertical_spacing

        sys.stdout.write('\033[F' * len(options))

    if(os.name == 'nt'):
        os.system("cls")
        cursor_info.visible = True
        ctypes.windll.kernel32.SetConsoleCursorInfo(_STD_OUTPUT_HANDLE, ctypes.byref(cursor_info))
    else:
        os.system("clear")
        sys.stdout.write("\033[?25h")

    return cursor_height - vertical_spacing