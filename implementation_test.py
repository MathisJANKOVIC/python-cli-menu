# import time
import pyclimenu

OPTIONS = ["Option 1", "Option 2", "Option 3", "Quit"]

# Creates a console menu with blue cursor and title on single line
choice1: str = pyclimenu.menu("Amazing Console Menu", OPTIONS, "blue")
