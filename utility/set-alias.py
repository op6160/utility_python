import os
import subprocess
import platform
from pathlib import Path
from src.utils.printer import log_msg

# ---------------------------------------------------------
# User-defined commands to set as aliases/functions
# ---------------------------------------------------------
command_set = {
    "save-req": "python -m pip freeze > requirements.txt",
    "pip-install": "pip install -r requirements.txt",
    "venv-create": "python -m venv venv",
    # venv activate set placeholder set to be replaced later based on OS
    "venv-on": "activate_placeholder", 
}

def get_windows_profile():
    """Get PowerShell profile path on Windows."""
    try:
        result = subprocess.run(
            ["powershell", "-Command", "echo $PROFILE"],
            capture_output=True, text=True, check=True
        )
        path = result.stdout.strip()
        return Path(path)
    except Exception:
        return None

def get_linux_profile():
    """Get .bashrc or .zshrc path on Linux/Mac."""
    shell = os.environ.get("SHELL", "")
    home = Path.home()
    if "zsh" in shell:
        return home / ".zshrc"
    else:
        return home / ".bashrc"

def format_command(os_type, alias_name, command_str):
    # venv activater set
    if command_str == "activate_placeholder":
        if os_type == "windows":
            command_str = ".\\venv\\Scripts\\activate"
        else:
            command_str = "source ./venv/bin/activate"

    # Syntax formatting
    if os_type == "windows":
        # Windows PowerShell
        return f'function {alias_name} {{ {command_str} }}'
    else:
        # Linux/Mac
        return f"alias {alias_name}='{command_str}'"

def main():
    current_os = platform.system() # 'Windows', 'Linux', 'Darwin'(Mac)
    
    target_profile = None
    os_type = ""

    # OS & shell profile detection
    if current_os == "Windows":
        os_type = "windows"
        target_profile = get_windows_profile()
        log_msg("Detected System: Windows (PowerShell)")
    
    elif current_os == "Linux" or current_os == "Darwin":
        os_type = "linux"
        target_profile = get_linux_profile()
        log_msg(f"Detected System: {current_os}")
        
    else:
        log_msg(f"Unsupported OS: {current_os}")
        return

    if not target_profile:
        log_msg("Could not find profile path.")
        return

    log_msg(f"Shell Profile Path: {target_profile}")

    # Generate content to write
    lines_to_write = []
    lines_to_write.append("\n# --- [Auto Generated Commands Start] ---")
    
    for name, cmd in command_set.items():
        formatted_line = format_command(os_type, name, cmd)
        lines_to_write.append(formatted_line)
        log_msg(f"   Prepared: {name} -> {cmd}")
        
    lines_to_write.append("# --- [Auto Generated Commands End] ---\n")

    # Write to profile file.
    try:
        # Create parent directories if they don't exist
        if not target_profile.parent.exists():
            target_profile.parent.mkdir(parents=True, exist_ok=True)

        with open(target_profile, "a", encoding="utf-8") as f:
            f.write("\n".join(lines_to_write))
        
        log_msg("\n All commands appended successfully!")
        
        if os_type == "windows":
            log_msg(" Run this to apply: . $PROFILE")
        else:
            log_msg(f" Run this to apply: source {target_profile}")
            
    except Exception as e:
        log_msg(f" Error writing to file: {e}")

if __name__ == "__main__":
    main()