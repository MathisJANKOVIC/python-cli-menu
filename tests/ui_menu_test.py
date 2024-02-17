from pythonclimenu.climenu import _Keys
import pythonclimenu
import pytest

import msvcrt
import os

MENU_OPTIONS = ["Option 1", "Option 2", "Option 3"]

KEYS = {
    "up": _Keys.UP["nt"],
    "down": _Keys.DOWN["nt"],
    "select": _Keys.SELECT,
}

def cursor_pattern(*moves):
    keys = iter([KEYS[move] for move in moves] + [KEYS["select"]])
    return lambda: next(keys)

class MockTerminalSize:
    def __init__(self, lines: int, columns: int):
        self.lines = lines
        self.columns = columns

@pytest.fixture
def mock_os_name(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(os, 'name', 'nt')

@pytest.fixture
def mock_terminal_to_classic_size(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(os, 'get_terminal_size', lambda: MockTerminalSize(24, 120))


def test_basic_menu_functionnality(mock_os_name, mock_terminal_to_classic_size, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(msvcrt, 'getwch', lambda: KEYS["select"])
    selected_option = pythonclimenu.menu("Test Menu", MENU_OPTIONS , "blue")
    assert selected_option == MENU_OPTIONS[0]

def test_menu_navigation(mock_os_name, mock_terminal_to_classic_size, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(msvcrt, 'getwch', cursor_pattern("down", "down", "down", "up", "up"))
    selected_option = pythonclimenu.menu("Test Menu", MENU_OPTIONS , "red")
    assert selected_option == MENU_OPTIONS[1]

def test_menu_navigation(mock_os_name, mock_terminal_to_classic_size, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(msvcrt, 'getwch', cursor_pattern("up"))
    selected_option = pythonclimenu.menu("Test Menu", MENU_OPTIONS , "red")
    assert selected_option == MENU_OPTIONS[2]