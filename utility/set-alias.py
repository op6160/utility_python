"""
Utility to set custom command aliases/functions in the user's shell profile automatically.
Supported OS: Windows(PowerShell), Linux, Mac (bash/zsh)

If you want delete previously added commands, remove the profile file or the section between:
# --- [Auto Generated Commands Start] ---
# --- [Auto Generated Commands End] ---
in the shell profile file. e.g., ~/.bashrc, ~/.zshrc, $PROFILE (PowerShell).
You can get profile file pathes using src.module.os_lib.get_shell_profile()

Raises:
    RuntimeError: If the shell profile path cannot be determined.
"""
import use_modules  # ensure module path is set     # type: ignore # noqa: F401 
from src.module.printer import log_msg
from src.module.os_lib import get_os_type, get_shell_profile
# Import user-defined command set 
from set_alias_config import command_set, placeholder_formatting

def format_command(os_type, alias_name, command_str):
    # venv activater set
    if "$placeholder" in str(command_str):
        log_msg(f"  (Replacing {command_str} based on OS...)")
        command_str = placeholder_formatting(os_type, command_str)
        
    log_msg(f"  Preparing: {alias_name} -> {command_str}")
    # Syntax formatting
    if os_type == "windows":
        # Windows PowerShell
        return f'function {alias_name} {{ {command_str} }}'
    else:
        # Linux/Mac
        return f"alias {alias_name}='{command_str}'"

def main():
    # get OS and shell profile path
    os_type = get_os_type()
    target_profile = get_shell_profile()

    if not target_profile:
        raise RuntimeError("Could not determine shell profile path.")
    log_msg(f"Detected System: {os_type}")

    # Generate content to write
    lines_to_write = []
    lines_to_write.append("\n# --- [Auto Generated Commands Start] ---")
    
    # Write each command
    for name, cmd in command_set.items():
        formatted_line = format_command(os_type, name, cmd)
        lines_to_write.append(formatted_line)
        # log_msg(f"   Prepared: {name} -> {cmd}")

    lines_to_write.append("# --- [Auto Generated Commands End] ---\n")

    # Write to profile file.
    try:
        # Create parent directories if they don't exist
        if not target_profile.parent.exists():
            target_profile.parent.mkdir(parents=True, exist_ok=True)

        with open(target_profile, "a", encoding="utf-8") as f:
            f.write("\n".join(lines_to_write))
        
        log_msg(" All commands appended successfully!")
        
        if os_type == "windows":
            log_msg("Run this to apply: . $PROFILE")
        else:
            log_msg(f"Run this to apply: source {target_profile}")
            
    except Exception as e:
        log_msg(f" Error writing to file: {e}")

if __name__ == "__main__":
    main()