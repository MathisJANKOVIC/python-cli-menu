# import time
import pyclimenu

OPTIONS = ["Option 1", "Option 2", "Option 3", "Quit", "option 4", "optin 11"]

# Creates a console menu with blue cursor and title on single line
choice1: str = pyclimenu.menu(["amazing", "console", "menu"], OPTIONS, "blue", title_color=["green", "red", (123, 3, 111)])

