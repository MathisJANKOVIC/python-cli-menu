# Console-GUI-Menu

Console GUI Menu is Python module for Windows that allows you to easilly create custom graphical user interface menu in the console. Customize the title, options, cursor color and initial cursor position. Use arrows keys to navigate through the menu and enter key to select an option.

![menu screen](/screen_menu.png)

## Quickstart

```python
def menu(
    title: str | list[str] | tuple[str, ...],
    options: list[str] | tuple[str, ...],
    cursor_color: str | tuple[int, int, int],
    initial_cursor_position: str | int = 0,
    output_format: type = str
) -> (str | int)
```
> Creates a console GUI menu with arrow key navigation and returns the selected option. Clears console once an option is selected.

- `title` is the main title of the menu, can be displayed on multiple lines if a list or a tuple is passed
- `options` is the list of actions or choices that can be selected
- `cursor_color` is the color of the cursor, available colors are `red`, `green`, `yellow`, `blue`, `magenta`, `cyan` and `white`, use custom color by providing a tuple containing color RGB values
- `intial_cursor_position` is the index of the element or the element in `options` where the initial cursor position is set (default position is first element)
- `output_format` is the output type of the function, default is `str`, which returns the selected element from `options`, pass `int` to get the index of the selected element

<label style="font-size: 15px;">Examples :</label>

```python
from console_menu import menu

OPTIONS = ["Option 1", "Option 2", "Option 3", "Quit"]

# Creates a console menu with blue cursor and title on single line
choice1: str = menu("Amazing Console Menu", OPTIONS, "blue")

# Creates a console menu with orange cursor and title on multiple lines
choice2: str = menu(["Amazing Console", "Menu"], OPTIONS, (255, 102, 0))

# Creates a console menu with red cursor default set on last option
choice3: str = menu("Amazing Console Menu", OPTIONS, "red", initial_cursor_position=-1)

# Creates a console menu with yellow cursor and returns the index of selected option
choice4: int = menu("Amazing Console Menu", OPTIONS, "yellow", ouput_format=int)
```
## Requirements
- Windows
- Python 3.10+

## Configuration

To use the library, simply download `console_menu.py` and place it in your project directory. Alternatively, you can move the file to your Python library directory, allowing you to use the module in any project. Here are common locations for the library directory, where `XX` stands for your Python version :

- `C:\Program Files\PythonXX\Lib`
- `C:\Users\Username\AppData\Local\Programs\Python\PythonXX\Lib`
