from .climenu import menu
import platform

__python_version = platform.python_version_tuple()

if(int(__python_version[0]) != 3 or int(__python_version[1]) < 10):
    raise RuntimeError(
        "Python 3.10 or a newer version is required"
    )