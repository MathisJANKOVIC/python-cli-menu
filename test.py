BG_COLORS = {
    "red": "\033[41m",
    "green": "\033[42m",
    "yellow": "\033[43m",
    "blue": "\033[44m",
    "magenta": "\033[45m",
    "cyan": "\033[46m",
    "white": "\033[47m",
    "default": "\033[0m"
}

# menu("Hello World", ["option 1", "option 2", "option 3"], "blue", options_color="blue")
# menu("Hello World", ["option 1", "option 2", "option 3"], "blue", options_color=(190, 122, 75))
# menu("Hello World", ["option 1", "option 2", "option 3"], "blue", options_color=["blue", "yellow", "green"])
# menu("Hello World", ["option 1", "option 2", "option 3"], "blue", options_color=("blue", "yellow", "green"))
# menu("Hello World", ["option 1", "option 2", "option 3"], "blue", options_color=("blue", "yellow", "green"))
# menu("Hello World", ["option 1", "option 2", "option 3"], "blue", options_color=[(190, 122, 75), (190, 122, 75), "green"])
# menu("Hello World", ["option 1", "option 2", "option 3"], "blue", options_color=((190, 122, 75), (190, 122, 75), "green"))

def test(options_color: str | tuple[int, int, int] | list[str | tuple[int, int, int]] | tuple[str | tuple[int, int, int], ...] = "default"):

    if(type(options_color) is str and options_color in BG_COLORS.keys()):
        options_color = BG_COLORS[options_color]
    elif(type(options_color) is tuple and all(not isinstance(value, (str, tuple)) for value in options_color)):
        if(all(type(value) is int for value in options_color) and len(options_color) == 3 and 0 <= options_color[0] < 256 and 0 <= options_color[1] < 256 and 0 <= options_color[2] < 256):
            options_color = f"\033[48;2;{options_color[0]};{options_color[1]};{options_color[2]}m"
        else:
            raise ValueError(f"{options_color} are not valid RGB values for argument 'options_color' (values should be 3 integers between 0 and 255)")
    elif(isinstance(options_color, (list, tuple)) and all(((type(color) is str and color in BG_COLORS.keys()) or (type(color) is tuple and len(color) == 3 and all(type(rgb_value) is int and 0 <= rgb_value < 256 and 0 <= rgb_value < 256 and 0 <= rgb_value < 256 for rgb_value in color))) for color in options_color)):
        print("ok")
    else:
        print("non")

test(options_color=((190, 122, 75), (190, 122, 75), "green"))