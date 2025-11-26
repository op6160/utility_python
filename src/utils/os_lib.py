import os
import platform
import sys
import subprocess
from pathlib import Path

def get_os_type():
    """Get the current operation system type.
    """

    current_os = platform.system()
    if current_os == "Windows":
        return "windows"
    elif current_os == "Linux":
        return "linux"
    elif current_os == "Darwin":
        return "mac"
    else:
        return "unknown"

def get_shell_type():
    """Get the current shell type.
    """
    shell = os.environ.get("SHELL", "")
    if "zsh" in shell:
        return "zsh"
    elif "bash" in shell:
        return "bash"
    elif "powershell" in shell.lower():
        return "powershell"
    else:
        return "unknown"

def get_shell_profile():
    """Get the shell profile path based on OS and shell type.
    """
    os_type = get_os_type()
    if os_type == "windows":
        try:
            result = subprocess.run(
                ["powershell", "-Command", "echo $PROFILE"],
                capture_output=True, text=True, check=True
            )
            path = result.stdout.strip()
            return Path(path)
        except Exception:
            return None
    else:
        shell_type = get_shell_type()
        home = Path.home()
        if shell_type == "zsh":
            return home / ".zshrc"
        else:
            return home / ".bashrc"