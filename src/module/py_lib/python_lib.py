import sys
import os

_frame = sys._getframe()

def get_python_filename():
    return os.path.basename(_frame.f_code.co_filename)

def get_python_codeline():
    return _frame.f_lineno