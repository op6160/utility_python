# ---------------------------------------------------------
# User-defined commands to set as aliases/functions
# ---------------------------------------------------------

# Example of how to add custom commands
command_set = {
    "save-req": "python -m pip freeze > requirements.txt",
    "pip-install": "pip install -r requirements.txt",
    "venv-create": "python -m venv venv",
    # venv activate set placeholder set to be replaced later based on OS.
    # If you want to add more commands with placeholders, follow this pattern. : "$placeholder" in custom command
    # And you must also add the handling logic in placeholder_formatting function.
    "venv-on": "activate_$placeholder",
}

# placeholder formatting function
def placeholder_formatting(os_type, command_str):
    command_replaced = None
    if command_str == "activate_$placeholder":
        if os_type == "windows":
            command_replaced = ".\\venv\\Scripts\\activate"
        else:
            command_replaced = "source ./venv/bin/activate"
    # ----------------------------------------------------------- #
    # Add more placeholders here as needed. use elif structure.
    # example
    elif command_str == "another_$placeholder": 
        if os_type == "windows":
            command_replaced = "..."
        else:
            command_replaced = "..."
    # elif command_str == "yet_another_$placeholder":
        # ...
    # ----------------------------------------------------------- #
    # unknown placeholder
    if command_replaced is None:
        raise ValueError(f"Unknown placeholder command: {command_str}")
    return command_replaced

# execution : python set-alias.py