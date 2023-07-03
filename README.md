# Console-GUI-Menu

Console GUI Menu is Python module that allows you to easilly create a graphical user interface menu on console without any external library. You can select an option by moving the cursor using arrow keys.

The module provides a function that allows you to create the menu and custom the title, options and cursor color. The function returns the selected option. Available colors are red, green, yellow, blue, magenta, cyan. You can also use a custom color by specifing ANSI color code using octal escape code starting with '\033'.

![qsd](/screen_menu.png)

## Quickstart

```python
import console_menu as cm

OPTIONS = ["Option 1", "Option 2", "Option 3", "Quit"]

# Creates a console menu with blue cursor
choice1 = cm.console_menu(title="Amazing Console Menu", options=OPTIONS, cursor_color="blue")

# Creates a console menu with white cursor
choice2 = cm.console_menu(title="Amazing Console Menu 2", options=OPTIONS, cursor_color="\033[47m")

print(choice1) # output : "Option 1"
```

## Requirements
- Git (optionnal)
- Python

## Configuration

To use the librairy you can simply download console_menu.py and move it in your project or move the file into your python librairy directory to use the module everywhere. Here are common locations for python librairies directory where 'X' stands for your python version :

- Windows : ```C:\Program Files\PythonX\Lib``` or ```C:\Users\Username\AppData\Local\Programs\Python\PythonX\Lib```
- MacOS : ```~/Library/Python/X/lib/pythonX``` or ```/Library/Frameworks/Python.framework/Versions/X/lib/pythonX```
- Linux : ```/usr/lib/pythonX```
