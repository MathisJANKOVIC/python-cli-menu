import sys
import os

class Keys:
    ARROW_UP = b'H'
    ARROW_DOWN = b'P'
    ENTER = b'\r'

ANSI_BG_COLORS = {
    "red": '\033[41m',
    "green": '\033[42m',
    "yellow": '\033[43m',
    "blue": '\033[44m',
    "magenta": '\033[45m',
    "cyan": '\033[46m',
    "white": '\033[47m'
}

def create_menu(title: str | list | tuple, options: list | tuple, cursor_color: str) -> str :
    """Creates a console GUI menu with a cursor and returns the selected option. Pass a list or a tuple to 'title' to print the title on multiple lines. Use arrow keys to move the cursor.
    Cursor colors available : red, green, yellow, blue, magenta, cyan.
    You can use a custom color by specifing ANSI color code using octal escape code '\\033'. """

    TERMINAL_HEIGHT = os.get_terminal_size().lines
    TERMINAL_WIDTH = os.get_terminal_size().columns

    VERTICAL_SPACING = (TERMINAL_HEIGHT - len(options)) // 2
    cursor_height = VERTICAL_SPACING

    if(not cursor_color.startswith('\033')):
        if(ANSI_BG_COLORS.get(cursor_color) == None):
            raise ValueError(f"'{cursor_color}' is not a valid option for cursor color please check the function documentation.")
        else:
            cursor_color = ANSI_BG_COLORS.get(cursor_color)

    os.system("cls" if os.name == 'nt' else "clear")
    sys.stdout.write('\033[?25l') # Hides cursor

    if(type(title) == str):
        title_height = 1
    else:
        title_height = len(title)

    key: bytes = None
    while(key != Keys.ENTER):

        print('\n'*(VERTICAL_SPACING - title_height - 2))

        if(type(title) == str):
            print(" " + title.center(TERMINAL_WIDTH - 1))
            sys.stdout.write('\n\n')
        else:
            for line in title:
                print(" " + line.center(TERMINAL_WIDTH - 1))
            sys.stdout.write('\n')

        for line, option in enumerate(options):
            if(line + VERTICAL_SPACING == cursor_height):
                print(" " + cursor_color + option.center(TERMINAL_WIDTH - 1) + '\033[0m')
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

        sys.stdout.write('\033[F' * (VERTICAL_SPACING + len(option) + title_height + 2))

    sys.stdout.write('\033[?25h') # show cursor
    os.system("cls" if os.name == "nt" else "clear")

    return options[cursor_height - VERTICAL_SPACING]

if(__name__ == "__main__"):
    OPTIONS = ["Option 1", "Option 2", "Option 3", "Quit"]
    choice = create_menu("Amazing Console Menu", OPTIONS, "red")
    print(choice)
