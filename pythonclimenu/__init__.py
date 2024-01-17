from .climenu import menu
import sys

__all__ = ["climenu"]

if(sys.version_info < (3, 10)):
    raise RuntimeError(
        "Python 3.10 or a newer version is required"
    )