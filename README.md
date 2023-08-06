# Console-GUI-Menu

Console GUI Menu is Python module for Windows that allows you to easilly create custom graphical user interface menu in the console. Customize the title, options, cursor color and initial cursor position. Use arrows keys to navigate through the menu and enter key to select an option.

![qsd](/screen_menu.png)

## Quickstart

<label style="font-size: 15px;"><b>menu</b>(title: str | list | tuple, options: list | tuple, cursor_color: str, initial_cursor_position: str=0 | int, output_format:type=str):</label>

> Creates a console GUI menu with arrow key navigation and clears console once an option is selected.

- `title` is the main title of the menu, can be displayed on multiple lines if a list or a tuple is passed
- `options` is the list of action or choices that can be selected with the cursor
- `cursor_color` is the color of the cursor, available colors are `red`, `green`, `yellow`, `blue`, `magenta`, `cyan` and `white`, use custom color by specifying ANSI color code using escape code `\033`
- `intial_cursor_position` is the index of element or  the element in `options` where the initial cursor position is set
- `output_format` is the output type of the function, if `str` returns the selected element from the options list, if `int` returns the index of the selected element.

```python
from console_menu import menu

OPTIONS = ["Option 1", "Option 2", "Option 3", "Quit"]

# Creates a console menu with blue cursor
choice1: str = menu("Amazing Console Menu", OPTIONS, cursor_color="blue")

# Creates a console menu with red cursor and title on multiple lines
choice2 = menu(title=["Amazing Console", "Menu 2"], options=OPTIONS, cursor_color="red")

# Creates a console menu with white cursor default set on last option
choice3 = menu(title="Amazing Console Menu", options=OPTIONS, cursor_color="\033[47m", initial_cursor_position=-1)

print(choice1) # output : "Option 1"
```
## Requirements

- Windows
- Python 3.10+

## Configuration

To use the library, simply download console_menu.py and place it in your project directory. Alternatively, you can move the file to your Python library directory, allowing you to use the module in any project just by importing the module. Here are common locations for the library directory, where 'XX' stands for your Python version :

- ```C:\Program Files\PythonXX\Lib```
- ```C:\Users\Username\AppData\Local\Programs\Python\PythonXX\Lib```
