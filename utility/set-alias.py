"""
Utility to set custom command aliases/functions in the user's shell profile automatically.
Supported OS: Windows(PowerShell), Linux, Mac (bash/zsh)

Raises:
    RuntimeError: If the shell profile path cannot be determined.
"""
from src.module.printer import log_msg
from src.module.os_lib import get_os_type, get_shell_profile

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
    os_type = get_os_type()
    target_profile = get_shell_profile()
    if not target_profile:
        raise RuntimeError("Could not determine shell profile path.")
    log_msg(f"Detected System: {os_type}")

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