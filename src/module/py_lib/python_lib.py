import sys
import os

def get_python_filename():
    try:
        return os.path.basename(sys._getframe(1).f_code.co_filename)
    except (ValueError, AttributeError):
        return "unknown"

def get_python_codeline():
    try:
        return sys._getframe(1).f_lineno
    except (ValueError, AttributeError):
        return 0