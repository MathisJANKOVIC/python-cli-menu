from typing import Sequence
import sys
import os

if(os.name == 'nt'):
    import msvcrt
else:
    import termios
    import tty

def menu(
    title: str ,
    options: list[str] ,
    cursor_color: str ,
    options_color: str = None,
    initial_cursor_position: int = 0,
) -> int:

    """Creates a pretty menu in console. Use arrow keys to move the cursor and enter key to select an option.
    Clears console once an option is selected.

    Args:
        - title: main title of the menu, can be displayed on multiple lines if a list or a tuple is passed.
        - options: list of elements that can be selected by the user.
        - cursor_color: color of the cursor, available colors are `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white` and their lighter versions (e.g. `light_red`),
        use custom color by providing a tuple containing color RGB values.
        - options_color (optional): color of options text, available colors are the same as `cursor_color`,
        customize the color of every options separately by providing a list of colors,
        each color will be associated with the option of the corresponding index.
        - initial_cursor_position (optional): index of element in `options` where the initial cursor position is set
        (default position is first element).

    Returns:
       - selected_option: index of element from `options` selected by the user.
    """
    class Keys:
        UP = ['H', '\x1b[A']
        DOWN = ['P', '\x1b[B']
        SELECT = '\r'

    DEFAULT_COLORS = ("default", "red", "green", "yellow", "blue", "magenta", "cyan", "white")

    def ansi(color: str , bg: bool, rgb: bool = False):
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
    elif(any(type(element) is not str for element in options)):
        raise TypeError(
            "all elements of menu() argument 'options' must be str"
        )

    TERMINAL_HEIGHT = os.get_terminal_size().lines
    TERMINAL_WIDTH = os.get_terminal_size().columns

    VERTICAL_SPACING = (TERMINAL_HEIGHT - len(options)) // 2

    if(type(title) is str and len(options) + 3 >= TERMINAL_HEIGHT):
        raise RuntimeError(
           "terminal height is too low to display all options, resize your terminal or reduce the number of options"
        )
    elif(len(options) + 3 >= TERMINAL_HEIGHT):
        raise RuntimeError(
           "terminal height is too low to display all options, resize your terminal or reduce the number of options"
        )

    if(type(cursor_color) not in (str, tuple)):
        raise TypeError(
            f"menu() argument 'cursor_color' expects str or tuple, not {type(cursor_color).__name__}"
        )
    elif(type(cursor_color) is tuple):
        if(len(cursor_color) == 3 and all(type(value) is int and 0 <= value < 256 for value in cursor_color)):
            ansi_cursor_color = ansi(cursor_color, rgb=True, bg=True)
        else:
            raise ValueError(
                "menu() argument 'cursor_color' has invalid RGB values"
            )
    elif(type(cursor_color) is str and cursor_color.removeprefix("light_") in DEFAULT_COLORS):
        ansi_cursor_color = ansi(cursor_color, bg=True)
    else:
        raise ValueError(
            "menu() argument 'cursor_color' has an invalid color"
        )

    if(not isinstance(options_color, Sequence) and options_color is not None):
        raise TypeError(
            f"menu() argument 'options_color' expects str, list, tuple or None, not {type(options_color).__name__}"
        )
    elif(options_color is None):
        multiple_colors_for_options = False
        ansi_options_color = ""

    elif(type(options_color) is str and options_color.removeprefix("light_") in DEFAULT_COLORS):
        multiple_colors_for_options = False
        ansi_options_color = ansi(options_color, bg=False)

    elif(type(options_color) is tuple and all(type(value) is int for value in options_color)):
        if(len(options_color) == 3 and all(type(value) is int and 0 <= value < 256 for value in options_color) ):
            multiple_colors_for_options = False
            ansi_options_color = ansi(options_color, rgb=True, bg=False)
        else:
            raise ValueError(
                "menu() argument 'options_color' has invalid RGB values"
            )
    elif(type(options_color) in (list, tuple)):
        if(all(((type(color) is str and color.removeprefix("light_") in DEFAULT_COLORS)
                or (type(color) is tuple and len(color) == 3 and all(type(rgb_value) is int and 0 <= rgb_value < 256 for rgb_value in color))
                or color is None) for color in options_color)):

            if(len(options_color) <= len(options)):
                multiple_colors_for_options = True
                ansi_options_color = []

                for color in options_color:
                    if(color is None):
                        ansi_options_color.append("")
                    elif(type(color) is str):
                        ansi_options_color.append(ansi(color, bg=False))
                    else:
                        ansi_options_color.append(ansi(color, rgb=True, bg=False))

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
            cursor_height = VERTICAL_SPACING + options.index(options[initial_cursor_position])
        else:
            raise ValueError(
                f"'{initial_cursor_position}' is not an index of menu() argument 'options'"
                )
    elif(type(initial_cursor_position) is str):
        if(initial_cursor_position in options):
            cursor_height = VERTICAL_SPACING + options.index(initial_cursor_position)
        else:
            raise ValueError(
                f"'{initial_cursor_position}' is not an element of menu() argument 'options'"
            )
    else:
        raise TypeError(
            f"menu() argument 'initial_cursor_position' expects int or str, not {type(initial_cursor_position).__name__}"
        )

    if(os.name == 'nt'):
        os.system("cls")
    else:
        os.system("clear")
        fd = sys.stdin.fileno()
        original_settings = termios.tcgetattr(fd)

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
        if(multiple_colors_for_options):
            for line, option in enumerate(options):
                if(line + VERTICAL_SPACING == cursor_height):
                    print(" " + ansi_cursor_color + ansi_options_color[line] + option.center(TERMINAL_WIDTH - 1) + "\033[0m")
                else:
                    print(" " + ansi_options_color[line] + option.center(TERMINAL_WIDTH - 1) + "\033[0m")
        else:
            for line, option in enumerate(options):
                if(line + VERTICAL_SPACING == cursor_height):
                    print(" " + ansi_cursor_color + ansi_options_color + option.center(TERMINAL_WIDTH - 1) + "\033[0m")
                else:
                    print(" " + ansi_options_color + option.center(TERMINAL_WIDTH - 1) + "\033[0m")

        if(os.name == 'nt'):
            key = msvcrt.getwch()
        else:
            tty.setraw(fd)
            char1 = sys.stdin.read(3)

            if(char1 == '\x1b'):
                char2 = sys.stdin.read(1)
                char3 = sys.stdin.read(1)

                key = char1 + char2 + char3
            else:
                key = char1

            termios.tcsetattr(fd, termios.TCSADRAIN, original_settings)

        if(key in Keys.UP):
            if(cursor_height > VERTICAL_SPACING):
                cursor_height = cursor_height - 1
            else:
                cursor_height = VERTICAL_SPACING + len(options) - 1
        elif(key in Keys.DOWN):
            if(cursor_height < VERTICAL_SPACING + len(options) - 1):
                cursor_height = cursor_height + 1
            else:
                cursor_height = VERTICAL_SPACING

        sys.stdout.write('\033[F' * len(options))

    sys.stdout.write("\033[?25h") # show cursor
    os.system("cls" if os.name == 'nt' else "clear")

    return options[cursor_height - VERTICAL_SPACING]