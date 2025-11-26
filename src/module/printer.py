import sys
import os
from pathlib import Path
from src.module.time_lib import detail

class MessageFormatter:
    """"A callable class to format and print messages with optional file logging.

    Attributes:
        header (str): Text to prepend to each message.
        footer (str): Text to append to each message.
        file_path (str or None): If provided, messages will be appended to this file.
    Methods:
        __call__(msg): Formats and prints the message, and writes to file if specified.
        override(...): Returns a new MessageFormatter with modified header/footer/file_path.
        get(): Returns current configuration as a dictionary.
    """
    def __init__(self, header="", footer="", file_path=None):
        self._header = str(header)
        self._footer = str(footer)
        self.file_path = file_path # Log file path

    def __call__(self, msg):
        # Formatting
        full_msg = f"{self.header}{str(msg)}{self.footer}"
        
        # Console print
        print(full_msg)

        # write file if path is given
        if self.file_path:
            self._write_to_file(full_msg)

    def _write_to_file(self, msg):
        """Logic to write message to a file."""
        try:
            path_obj = Path(self.file_path)
            if not path_obj.parent.exists():
                path_obj.parent.mkdir(parents=True, exist_ok=True)

            with open(self.file_path, "a", encoding="utf-8") as f:
                f.write(msg + "\n")
        except Exception as e:
            print(f"[Log Error] Failed to save file.: {e}")

    def __repr__(self):
        header = f"header='{self._header}'" if self._header else ""
        footer = f"footer='{self._footer}'" if self._footer else ""
        file_p = f"file_path='{self.file_path}'" if self.file_path else ""
        
        params = [p for p in [header, footer, file_p] if p]
        return f"MessageFormatter({', '.join(params)})"

    @property
    def header(self):
        """Get or set the header text."""
        return self._header
    @header.setter
    def header(self, value):
        self._header = str(value)

    @property
    def footer(self):
        """Get or set the footer text."""
        return self._footer
    @footer.setter
    def footer(self,value):
        self._footer = str(value)

    def override(self, header="", footer="", header_option="back", footer_option="back", file_path=None):
        """
        Create a new MessageFormatter with overridden header/footer/file_path.
        Args:
            header (str): New header text to add.
            footer (str): New footer text to add.
            header_option (str): "back" to append, "front" to prepend the new header.
            footer_option (str): "back" to append, "front" to prepend the new footer.
            file_path (str or None): New file path for logging. If None, keeps the current path.
        Returns:
            MessageFormatter: A new instance with updated settings.
        """
        # header
        new_header = self._header
        if header:
            if header_option == "back":
                new_header = self._header + str(header)
            elif header_option == "front":
                new_header = str(header) + self._header
        
        # footer
        new_footer = self._footer
        if footer:
            if footer_option == "back":
                new_footer = self._footer + str(footer)
            elif footer_option == "front":
                new_footer = str(footer) + self._footer

        # Set file_path
        final_file_path = file_path if file_path else self.file_path

        return MessageFormatter(header=new_header, footer=new_footer, file_path=final_file_path)

    def get(self) -> dict:
        return {"header": self.header, "footer": self.footer, "file_path": self.file_path}

MSGFormatter = MessageFormatter

def make_print_formatter(header='', footer='', file_path=None):
    header = str(header)
    footer = str(footer)

    def printer(msg):
        full_msg = f"{header}{str(msg)}{footer}"
        print(full_msg)
        
        if file_path:
            try:
                with open(file_path, "a", encoding="utf-8") as f:
                    f.write(full_msg + "\n")
            except Exception:
                pass # silently ignore file write errors

    return printer

_frame = sys._getframe()
python_filename = os.path.basename(_frame.f_code.co_filename)
python_codeline = _frame.f_lineno
detailtime = detail

# usage examples
# basic logger(print only)
log_msg = MessageFormatter(header=f"[{detailtime}] ")

# debug logger (with file saving)
debug = log_msg.override(
    header="[DEBUG] ", 
    file_path="logs/debug.log"
)
# function usage example
warning = make_print_formatter(
    header=f"[{python_filename}: {python_codeline}lines] Warning:", 
)

if __name__ == "__main__":    
    log_msg("print only user log.")
    debug("print and save debug.log file.")
    warning("print only warning message.")