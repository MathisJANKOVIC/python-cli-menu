import os

class Keys:
    ARROW_UP = b"H"
    ARROW_DOWN = b"P"
    ENTER = b'\r'

ANSI_BG_COLORS = {
    "red": "\033[41m",
    "green": "\033[42m",
    "yellow": "\033[43m",
    "blue": "\033[44m",
    "magenta": "\033[45m",
    "cyan": "\033[46m",
    "white": "\033[47m"
}

def console_menu(title: str, options: tuple | list, cursor_color: str) -> str :
    """Creates a console GUI menu with a cursor and returns the selected option. Use arrow keys to move the cursor.
    Cursor colors available : red, green, yellow, blue, magenta, cyan. You can use a custom color by specifing ANSI color code using octal escape code '\\033'"""

    TERMINAL_HEIGHT = os.get_terminal_size().lines
    TERMINAL_WIDTH = os.get_terminal_size().columns

    VERTICAL_SPACING = (TERMINAL_HEIGHT - len(options)) // 2
    cursor_height = VERTICAL_SPACING
    key = None

    if(not cursor_color.startswith("\033")):
        if(ANSI_BG_COLORS.get(cursor_color) == None):
            raise ValueError(f"'{cursor_color}' is not a valid option for cursor color please check the function documentation.")
        else:
            cursor_color = ANSI_BG_COLORS.get(cursor_color)

    os.system("cls" if os.name == "nt" else "clear")

    print('\033[?25l', end="") # Hides cursor

    while(key != Keys.ENTER):
        print("\n"*(VERTICAL_SPACING - 3))
        print(" " + title.center(TERMINAL_WIDTH - 1))
        print("\n")

        for i, option in enumerate(options):
            if(i + VERTICAL_SPACING == cursor_height):
                print(" " + cursor_color + option.center(TERMINAL_WIDTH - 1) + "\033[0m")
            else:
                print(" " + option.center(TERMINAL_WIDTH - 1))

        if(os.name == "nt"):
            import msvcrt
            key = msvcrt.getch()
        else:
            import readline
            readline.getch()

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

    print('\033[?25h', end="") # show cursor
    os.system("cls" if os.name == "nt" else "clear")

    return options[cursor_height - VERTICAL_SPACING]

if(__name__ == "__main__"):
    OPTIONS = ["Option 1", "Option 2", "Option 3", "Quit"]
    choice = console_menu("Amazing Console Menu", OPTIONS, "red")
    print(choice)
