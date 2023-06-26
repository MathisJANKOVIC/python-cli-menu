import colorama
import msvcrt
import os

class Keys:
    ARROW_UP = b"H"
    ARROW_DOWN = b"P"
    ENTER = b'\r'

def console_menu(title: str, options: tuple | list, cursor_color: str) -> str :
    """Creates a console GUI menu with a cursor and returns the selected option. Use arrow keys to move the cursor.
    Cursor colors available : black, red, green, yellow, blue, magenta, cyan, white, lightblack, lightred, lightgreen, lightyellow, lightblue, lightmagenta, lightcyan, lightwhite"""

    TERMINAL_HEIGHT = os.get_terminal_size().lines
    TERMINAL_WIDTH = os.get_terminal_size().columns

    VERTICAL_SPACING = (TERMINAL_HEIGHT - len(options)) // 2
    cursor_height = VERTICAL_SPACING
    key = None

    if("light" in cursor_color):
        colorama_cursor_color = cursor_color.upper() + "_EX"
    else:
        colorama_cursor_color = cursor_color.upper()

    try:
        colorama_color = getattr(colorama.Back, colorama_cursor_color)
    except AttributeError:
        raise ValueError(f"'{cursor_color}' is not a valid option for cursor color, please check the function doc")

    os.system("cls" if os.name == 'nt' else "clear")
    print('\033[?25l', end="") # Hides cursor

    while(key != Keys.ENTER):
        print("\n"*(VERTICAL_SPACING - 3))
        print(title.center(TERMINAL_WIDTH))
        print("\n")

        for i, option in enumerate(options):
            if(i + VERTICAL_SPACING == cursor_height):
                print(colorama_color + option.center(TERMINAL_WIDTH) + colorama.Back.BLACK)
            else:
                print(option.center(TERMINAL_WIDTH))

        while(not msvcrt.kbhit()):
            pass

        key = msvcrt.getch()

        if(key == Keys.ARROW_UP):
            if(cursor_height > VERTICAL_SPACING):
                cursor_height = cursor_height - 1
            else:
                cursor_height = VERTICAL_SPACING + len(options) - 1
        elif(key == Keys.ARROW_DOWN):
            if(cursor_height < VERTICAL_SPACING + len(options) - 1):
                cursor_height = cursor_height + 1
            else:
                cursor_height = VERTICAL_SPACING

        print("\033[F" * (len(options) + VERTICAL_SPACING + 3), end="")
    print('\033[? 25h', end="")

    return options[cursor_height - VERTICAL_SPACING]

if(__name__ == "__main__"):
    OPTIONS = ["Option 1", "Option 2", "Option 3", "Quit"]
    choice = console_menu("Welcome", OPTIONS, "lightblue")
    print(choice)
