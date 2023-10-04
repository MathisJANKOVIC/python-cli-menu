import msvcrt
import sys
import os

class Keys:
    UP = 'H' # Arrow up
    DOWN = 'P' # Arrow down
    SELECT = '\r' # Enter

DEFAULT_COLORS = ("default", "red", "green", "yellow", "blue", "magenta", "cyan", "white")

def ansi_escape_code(color: str | tuple, rgb: bool = False, bg: bool = False):
    if(rgb):
        if(bg):
            return f"\033[48;2;{color[0]};{color[1]};{color[2]}m"
        else:
            return f"\033[38;2;{color[0]};{color[1]};{color[2]}m"
    else:
        if(color.startswith("light")):
            index = DEFAULT_COLORS.index(color.removeprefix("light_"))
            if(bg):
                return f"\033[10{index}m"
            else:
                return f"\033[9{index}m"
        else:
            index = DEFAULT_COLORS.index(color)
            if(bg):
                return f"\033[4{index}m"
            else:
                return f"\033[3{index}m"

def menu(
    title: str | list[str] | tuple[str, ...],
    options: list[str] | tuple[str, ...],
    cursor_color: str | tuple[int, int, int],
    options_color: str | tuple[int, int, int] | list[str | tuple[int, int, int]] | tuple[str | tuple[int, int, int], ...] = "",
    initial_cursor_position: str | int = 0,
) -> str | int:

    """Creates a pretty graphical user interface menu in console, allowing users to navigate through the menu using arrow keys
    and select an option with enter key. Clears console once an option is selected.

    Args:
        - title: main title of the menu, can be displayed on multiple lines if a list or a tuple is passed
        - options: list of choices or actions that can be selected
        - cursor_color: color of the cursor, available colors are `red`, `green`, `yellow`, `blue`, `magenta`, `cyan` and `white`,
        use custom color by providing a tuple containing color RGB values
        - options_color: color of options text, available colors are the same as `cursor_color`,
        customize the color of every options separately by providing a list of colors,
        each color will be associated with the index of the corresponding option
        - initial_cursor_position (optional): index of element or element in `options` where the initial cursor position is set
        (default position is first element)
        - output_format (optionnal): output type of the function, default is `str`, which returns the selected element from `options`,
        pass `int` to get the index of the selected element

    Returns:
       - selected_option: element from `options` selected by the user if output_format is `str` else returns the index of the element
    """

    if(type(title) not in (str, list, tuple)):
        raise TypeError(f"argument 'title' expects str, list or tuple not {title.__class__.__name__}")
    elif(len(title) == 0):
        raise ValueError("argument 'title' cannot be empty")
    elif(type(title) in (list, tuple) and any(type(line) is not str for line in title)):
        raise TypeError("all elements of argument 'title' must be str")

    if(type(options) not in (list, tuple)):
        raise TypeError(f"argument 'options' expects list or tuple not {options.__class__.__name__}")
    elif(len(options) == 0):
        raise ValueError("argument 'options' cannot be empty")
    elif(any(type(element) is not str for element in options)):
        raise TypeError("all elements of argument 'options' must be str")

    TERMINAL_HEIGHT = os.get_terminal_size().lines
    TERMINAL_WIDTH = os.get_terminal_size().columns

    VERTICAL_SPACING = (TERMINAL_HEIGHT - len(options)) // 2

    if(type(cursor_color) not in (str, tuple)):
        raise TypeError(f"argument 'cursor_color' expects str or tuple not {cursor_color.__class__.__name__}")
    elif(type(cursor_color) is str and cursor_color.removeprefix("light_") in DEFAULT_COLORS):
        cursor_color = ansi_escape_code(cursor_color, bg=True)
    elif(type(cursor_color) is tuple):
        if(len(cursor_color) == 3 and all(type(value) is int and 0 <= value < 256 for value in cursor_color)):
            cursor_color = ansi_escape_code(cursor_color, rgb=True, bg=True)
        else:
            raise ValueError(f"{cursor_color} are not valid RGB values for argument 'cursor_color' (values should be 3 integers between 0 and 255)")
    else:
        raise ValueError(f"'{cursor_color}' is not a valid color for argument 'cursor_color' please check the function documentation.")

    if(type(options_color) not in (str, tuple, list)):
        raise TypeError(f"argument 'options_color' expects str, list or tuple not {options_color.__class__.__name__}")
    elif(type(options_color) is str and options_color.removeprefix("light_") in DEFAULT_COLORS):
        options_color = ansi_escape_code(options_color)
        has_options_single_color = True
    elif(options_color == ""):
        has_options_single_color = True
    elif(type(options_color) is tuple and all(not isinstance(value, (str, tuple)) for value in options_color)):
        if(all(type(value) is int for value in options_color) and len(options_color) == 3 and 0 <= options_color[0] < 256 and 0 <= options_color[1] < 256 and 0 <= options_color[2] < 256):
            options_color = ansi_escape_code(options_color, rgb=True)
            has_options_single_color = True
        else:
            raise ValueError(f"{options_color} are not valid RGB values for argument 'options_color' (values should be 3 integers between 0 and 255)")
    elif(isinstance(options_color, (list, tuple)) and all(((type(color) is str and color.removeprefix("light_") in DEFAULT_COLORS) or (type(color) is tuple and len(color) == 3 and all(type(rgb_value) is int and 0 <= rgb_value < 256 and 0 <= rgb_value < 256 and 0 <= rgb_value < 256 for rgb_value in color))) for color in options_color)):
        has_options_single_color = False
        for i, value in enumerate(options_color):
            if(type(value) is str):
                options_color[i] = ansi_escape_code(value)
            else:
                options_color[i] = ansi_escape_code(value, rgb=True)
    elif(options_color != ""):
        raise ValueError(f"'{options_color}' is not a valid option for argument 'options_color' please check the function documentation.")

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

        if(has_options_single_color):
            for line, option in enumerate(options):
                if(line + VERTICAL_SPACING == cursor_height):
                    print(cursor_color + option.center(TERMINAL_WIDTH - 1) + '\033[0m')
                else:
                    print(options_color + option.center(TERMINAL_WIDTH - 1))
        else:
            for line, option in enumerate(options):
                if(line + VERTICAL_SPACING == cursor_height):
                    print(options_color[line] + cursor_color + option.center(TERMINAL_WIDTH - 1) + '\033[0m')
                else:
                    print(options_color[line] + option.center(TERMINAL_WIDTH - 1))

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

    return options[cursor_height - VERTICAL_SPACING]