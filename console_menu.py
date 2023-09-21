import msvcrt
import sys
import os

class Keys:
    UP = 'H' # Arrow up
    DOWN = 'P' # Arrow down
    SELECT = '\r' # Enter

ANSI_BG_COLORS = {
    "red": "\033[41m",
    "green": "\033[42m",
    "yellow": "\033[43m",
    "blue": "\033[44m",
    "magenta": "\033[45m",
    "cyan": "\033[46m",
    "white": "\033[47m"
}

def menu(title: str | list[str] | list[str], options: list[str] | tuple[str, ...], cursor_color: str | tuple[int, int, int], initial_cursor_position: str | int = 0, output_format: type = str) -> str | int :
    """Creates a graphical user interface menu in console, allowing users to navigate through the menu using arrow keys and select an option with enter key. Clears console once an option is selected.

    Args:
        - `title`: main title of the menu, can be displayed on multiple lines if a list or a tuple is passed
        - `options`: list of choices or actions that can be selected
        - `cursor_color`: color of the cursor, available colors are `red`, `green`, `yellow`, `blue`, `magenta`, `cyan` and `white`, use custom color by providing a tuple containing color RGB values
        - `initial_cursor_position` (optional): index of element or element in `options` where the initial cursor position is set (default position is first element)
        - `output_format` (optionnal): output type of the function, default is `str`, which returns the selected element from `options`,
           pass `int` to get the index of the selected element

    Returns:
       - `selected_option`: element from `options` selected by the user if output_format is `str` else returns the index of the element"""

    if(type(title) is not str and type(title) is not list and type(title) is not tuple):
        raise TypeError(f"argument 'title' expects str, list or tuple not {title.__class__.__name__}")
    elif(isinstance(title, (list, tuple)) and not all(type(line) is str for line in title)):
        raise TypeError("all elements of argument 'title' must be str")
    elif(isinstance(title, (list, tuple)) and len(title) < 2):
        raise ValueError("argument 'title' if is a list or a tuple cannot have less than 2 elements")

    if(type(options) is not list and type(options) is not tuple):
        raise TypeError(f"argument 'options' expects list or tuple not {options.__class__.__name__}")
    elif(not all(type(element) is str for element in options)):
        raise TypeError("all elements of argument 'options' must be str")
    elif(len(options) < 2):
        raise ValueError("argument 'options' cannot have less than 2 elements")

    TERMINAL_HEIGHT = os.get_terminal_size().lines
    TERMINAL_WIDTH = os.get_terminal_size().columns

    VERTICAL_SPACING = (TERMINAL_HEIGHT - len(options)) // 2

    if(cursor_color in ANSI_BG_COLORS.keys()):
        cursor_color = ANSI_BG_COLORS[cursor_color]
    elif(type(cursor_color) is tuple and len(cursor_color) == 3 and all(type(value) is int for value in cursor_color)):
        if(0 <= cursor_color[0] < 256 and 0 <= cursor_color[1] < 256 and 0 <= cursor_color[2] < 256):
            cursor_color = f"\033[48;2;{cursor_color[0]};{cursor_color[1]};{cursor_color[2]}m"
        else:
            raise ValueError(f"{cursor_color} are not valid RGB values for argument 'cursor_color' (all values should be integers between 0 and 255)")
    else:
        raise ValueError(f"'{cursor_color}' is not a valid option for argument 'cursor_color' please check the function documentation.")

    if(type(initial_cursor_position) is int):
        if(-len(options) <= initial_cursor_position < len(options)):
            cursor_height = VERTICAL_SPACING + options.index(options[initial_cursor_position])
        else:
            raise ValueError(f"'{initial_cursor_position}' is not an index of argument 'options'")
    elif(type(initial_cursor_position) is str):
        if(initial_cursor_position in options):
            cursor_height = VERTICAL_SPACING + options.index(initial_cursor_position)
        else:
            raise ValueError(f"'{initial_cursor_position}' is not an element of argument 'options'")
    else:
        raise TypeError(f"argument 'initial_cursor_position' expects int or str not {initial_cursor_position.__class__.__name__}")

    if(output_format is not str and output_format is not int):
        raise ValueError(f"argument 'output_format', excpects type str or int not {output_format.__name__}")

    os.system("cls")
    sys.stdout.write("\033[?25l") # Hides cursor

    if(type(title) is str):
        print('\n'*(VERTICAL_SPACING - 3))
        print(" " + title.center(TERMINAL_WIDTH - 1) + '\n\n')
    else:
        print('\n'*(VERTICAL_SPACING - len(title) - 1))
        for line in title:
            print(" " + line.center(TERMINAL_WIDTH - 1))
        sys.stdout.write('\n')

    key = None
    while(key != Keys.SELECT):
        for line, option in enumerate(options):
            if(line + VERTICAL_SPACING == cursor_height):
                print(" " + cursor_color + option.center(TERMINAL_WIDTH - 1) + '\033[0m')
            else:
                print(" " + option.center(TERMINAL_WIDTH - 1))

        key = msvcrt.getwch()

        if(key == Keys.UP):
            if(cursor_height > VERTICAL_SPACING):
                cursor_height = cursor_height - 1
            else:
                cursor_height = VERTICAL_SPACING + len(options) - 1
        elif(key == Keys.DOWN):
            if(cursor_height < VERTICAL_SPACING + len(options) - 1):
                cursor_height = cursor_height + 1
            else:
                cursor_height = VERTICAL_SPACING

        sys.stdout.write('\033[F' * len(options))

    sys.stdout.write("\033[?25h") # show cursor
    os.system("cls")

    index_selected_option = cursor_height - VERTICAL_SPACING

    if(output_format is str):
        return options[index_selected_option]
    else:
        return index_selected_option