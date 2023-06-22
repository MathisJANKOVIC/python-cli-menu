import colorama
import msvcrt
import os

class Keys:
    ARROW_UP = b"H"
    ARROW_DOWN = b"P"
    ENTER = b'\r'

OPTIONS = ["Manger", "Dormir", "Sauvegarder", "Quitter"]

TERMINAL_HEIGHT = os.get_terminal_size().lines
TERMINAL_WIDTH = os.get_terminal_size().columns

VERTICAL_SPACING = (TERMINAL_HEIGHT - len(OPTIONS)) // 2
cursor_height = VERTICAL_SPACING # cursor initial position
key = None

os.system("cls")
print('\033[?25l', end="") # Hides cursor

while(key != Keys.ENTER):
    print("\n"*(VERTICAL_SPACING - 3))
    print("  Menu en console incroyable".center(TERMINAL_WIDTH))
    print("\n")

    for i, option in enumerate(OPTIONS):
        if(i + VERTICAL_SPACING == cursor_height):
            print(colorama.Back.BLUE + option.center(TERMINAL_WIDTH) + colorama.Back.BLACK)
        else:
            print(option.center(TERMINAL_WIDTH))

    while(not msvcrt.kbhit()):
        pass

    key = msvcrt.getch()

    if(key == Keys.ARROW_UP):
        if(cursor_height > VERTICAL_SPACING):
            cursor_height = cursor_height - 1  # Moves up the cursor
        else:
            cursor_height = VERTICAL_SPACING + len(OPTIONS) - 1 # Moves the cursor at the bottom of the list
    elif(key == Keys.ARROW_DOWN):
        if(cursor_height < VERTICAL_SPACING + len(OPTIONS) - 1):
            cursor_height = cursor_height + 1  # Moves down the cursor
        else:
            cursor_height = VERTICAL_SPACING # Moves the cursor at the top of the list

    print("\033[F" * (len(OPTIONS) + VERTICAL_SPACING + 2), end="")
print('\033[? 25h', end="")