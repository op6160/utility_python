import sys
import os
import subprocess
import importlib.util

def get_python_filename(depth: int = 1):
    try:
        return os.path.basename(sys._getframe(depth).f_code.co_filename)
    except (ValueError, AttributeError):
        return "unknown"

def get_python_codeline(depth: int = 1):
    try:
        return sys._getframe(depth).f_lineno
    except (ValueError, AttributeError):
        return 0

def install_lib(lib_name:str, install_name:str) -> bool:
    result = False
    spec = importlib.util.findspec(lib_name)
    if spec is None:
        print(f"{lib_name} not found. Installing...")
        result = subprocess.check_call([sys.executable, "-m", "pip", "install", install_name])
        try:
            importlib.import_module(lib_name)
            print(f"{lib_name} is installed successfully...")
            result = True
        except ImportError:
            print(f"Failed to import {lib_name}...")

    else:
        print(f"{lib_name} is installed already...")
    return result