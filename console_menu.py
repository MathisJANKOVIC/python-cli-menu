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

def create_menu(title: str | list | tuple, options: list | tuple, cursor_color: str, initial_cursor_position: int | str = 0) -> str:
    """Creates a GUI menu in console with a cursor that can be controlled by arrow keys. Clears console once user have selected an option.

    Args:
       - title : Main title of the menu. Pass a list or a tuple to print it on multiple lines.
       - options : Choices or actions that users can select.
       - cursor_color : Color of the cursor. Available colors are red, green, yellow, blue, magenta and cyan.
                        Use custom color by specifying ANSI color code using escape code '\\033'.
       - initial_cursor_position (optional) : Index of element or element in the list where the initial cursor position
                                              is set (default position is the first element).

    Returns:
       - str : element from the options list that is selected by the user """

    TERMINAL_HEIGHT = os.get_terminal_size().lines
    TERMINAL_WIDTH = os.get_terminal_size().columns

    VERTICAL_SPACING = (TERMINAL_HEIGHT - len(options)) // 2

    if(not cursor_color.startswith('\033')):
        if(ANSI_BG_COLORS.get(cursor_color) != None):
            cursor_color = ANSI_BG_COLORS[cursor_color]
        else:
            raise ValueError(f"'{cursor_color}' is not a valid option for cursor color please check the function documentation.")

    if(type(initial_cursor_position) == int):
        if(-len(options) <= initial_cursor_position < len(options)):
            cursor_height = VERTICAL_SPACING + options.index(options[initial_cursor_position])
        else:
            raise ValueError(f"'{initial_cursor_position}' is not an index of 'options'")
    elif(type(initial_cursor_position) == str):
        if(initial_cursor_position in options):
            cursor_height = VERTICAL_SPACING + options.index(initial_cursor_position)
        else:
            raise ValueError(f"'{initial_cursor_position}' is not an element of 'options'")
    else:
        raise TypeError(f"argument 'initial_cursor_position' expects int or str not {initial_cursor_position.__class__.__name__}")

    os.system("cls")
    sys.stdout.write("\033[?25l") # Hides cursor

    key = None
    while(key != Keys.SELECT):

        if(type(title) == str):
            print('\n'*(VERTICAL_SPACING - 3))
            print(" " + title.center(TERMINAL_WIDTH - 1) + '\n\n')
        else:
            print('\n'*(VERTICAL_SPACING - len(title) - 1))
            for line in title:
                print(" " + line.center(TERMINAL_WIDTH - 1))
            sys.stdout.write('\n')

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

        sys.stdout.write('\033[F' * TERMINAL_HEIGHT)

    sys.stdout.write("\033[?25h") # show cursor
    os.system("cls")

    return options[cursor_height - VERTICAL_SPACING]

