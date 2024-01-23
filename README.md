# python-cli-menu

`python-cli-menu` is a simple cross-plateform Python module that allows you to easilly create pretty custom menus in console. Customize the title, options, every colors and initial cursor position as you wish. Use arrows keys to navigate through the menu and enter key to select an option.

![menu screen](menu.png)

<p align="center">
    <img src="https://img.shields.io/badge/version-1.7-d" alt="version badge"/>
    <img src="https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20-blue" alt="python version badge"/>
    <img src="https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20MacOS-lightgray" alt="platform badge"/>
    <img src="https://img.shields.io/badge/license-MIT-yellow" alt="license badge"/>
    <img src="https://img.shields.io/github/contributors/MathisJANKOVIC/python-cli-menu?color=darkorange" alt="contributors badges"/>
</p>

## Installation
`python-cli-menu` is available on PyPi and can be installed with pip by running :
```bash
pip install python-cli-menu
```

## Quickstart

```python
def menu(
    title: str | Sequence[str],
    options: list[str] | tuple[str, ...],
    cursor_color: str | tuple[int, int, int],
    title_color: (
        str | tuple[int, int, int] | None |
        Sequence[str | tuple[int, int, int] | None]
    ) = None,
    options_color: (
        str | tuple[int, int, int] | None |
        Sequence[str | tuple[int, int, int] | None]
    ) = None,
    initial_cursor_position: str | int = 0,
) -> str:
```
> Creates a pretty menu in console with arrow key navigation and returns the selected option. Clears console once an option is selected.

- `title` is the main title of the menu, can be displayed on multiple lines if a list or a tuple is passed.
- `options` is the list of actions or choices that can be selected.
- `cursor_color` is the color of the cursor, available colors are `red`, `green`, `yellow`, `blue`, `magenta`, `cyan`, `white`
                and their lighter versions (e.g. `light_red`), use custom color by providing a tuple containing color RGB values.
- `title_color` is the color of the title, available colors are the same as `cursor_color`, customize the color of each line by providing a list of colors,
                each color will be associated with the line of the corresponding index (default color is terminal text color).
- `options_color` is the color of options, available colors are the same as `cursor_color`, customize every option color by providing a list of colors,
                each color will be associated with the option of the corresponding index (default color is terminal text color).
- `initial_cursor_position` is the option or the index of the option where the initial cursor position is set (default position is first element).

<label style="font-size: 15px;">Examples :</label>

```python
from pythonclimenu import menu

OPTIONS = ["Option 1", "Option 2", "Option 3", "Quit"]

# Creates a simple console menu with blue cursor
menu1 = menu(title="Amazing Console Menu", options=OPTIONS, cursor_color="blue")

menu2 = menu(
    title = ["Amazing Console", "Menu"], # displays title on multiple lines
    options = OPTIONS,
    cursor_color = (255, 95, 46), # sets the cursor color using RGB values
    title_color = [
        "blue", # colors "Amazing Console"
        "light_red" # colors "Menu"
    ],
    initial_cursor_position = -1 # sets cursor default position to 'Quit'
)

menu3 = menu(
    title = ["Amazing Console", "Menu"], # displays title on multiple lines
    options = OPTIONS,
    cursor_color = "yellow",
    title_color = "light_green", # colors all lines of title
    options_color = [
        "magenta", # colors options[0]
        "light_cyan", # colors options[1]
        (192, 11, 168) # colors options[2]
        # option[3] color is not specifed so it will be considered as None
    ],
    initial_cursor_position = OPTIONS[1] # sets cursor default position to 'Option 1'
)
```
