# Console-GUI-Menu

Console GUI Menu is Python module that allows you to easilly create a graphical user interface menu on console without any external library. You can select an option by moving the cursor using arrow keys.

The module provides a function that allows you to custom the title of the menu, the options and the cursor color. Available colors are red, green, yellow, blue, magenta, cyan. You can use a custom color by specifing ANSI color code using octal escape code '\033'

## Examples

```python
import console_menu as cm

OPTIONS = ["Option 1", "Option 2", "Option 3", "quit"]
choice = cm.console_menu(title="Amazing Console Menu", options=OPTIONS, cursor_color="blue")
```

<h3>Output :</h3>
<div style="text-align:center">
  <img src="Captured.PNG" alt="Nodm de l'image"/>
</div><br>

```python
import console_menu as cm

OPTIONS = ["Option 1", "Option 2", "Option 3", "quit"]
choice = cm.console_menu(title="Amazing Console Menu", options=OPTIONS, cursor_color="\033[48;5;202m")
```

<h3>Output :</h3>
<div style="text-align:center">
  <img src="Captured.PNG" alt="Nodm de l'image"/>
</div><br>

## Requirements
- Git (optionnal)
- Python

## Configuration
    1. Download and extract the zip or clone the project
    2. Navigate into a terminal to the project folder
    3. Run the command `python menu.py` (requires python path in environement variables)