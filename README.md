# Console-GUI-Menu

Console GUI Menu is Python module for Windows that allows you to easilly create a graphical user interface menu on console without the need for external libraries. You can navigate and select options by moving the cursor using arrow keys.

The module provides a function that allows you to create the menu with customizable title, options, cursor color and default cursor position. The function returns the selected option. You can pass a list or a tuple as the title parameter to print the title on multiple lines. Available colors for cursor are red, green, yellow, blue, magenta, cyan. You can also use a custom color by specifing ANSI color code using octal escape code starting with '\033'. To modify the initial cursor position, which is set on the first option by default, you can give either the index of the option or directly the option itself.

![qsd](/screen_menu.png)

## Quickstart

```python
from console_menu import menu

OPTIONS = ["Option 1", "Option 2", "Option 3", "Quit"]

# Creates a console menu with blue cursor
choice1 = menu(title="Amazing Console Menu", options=OPTIONS, cursor_color="blue")

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
