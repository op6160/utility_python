import sys
import os
from .module.logger_lib.formatter import MessageFormatter, make_print_formatter
from .time_lib import detail as __detailtime
from .py_lib import get_python_filename as __get_python_filename
from .py_lib import get_python_codeline as __get_python_codeline
MSGFormatter = MessageFormatter

# basic logger(print only)
log_msg = MessageFormatter(header=f"[{__detailtime}] ")

# debug logger (with file saving)
debug = log_msg.override(
    header="[DEBUG] ", 
    file_path="logs/debug.log"
)

# function usage example
warning = make_print_formatter(
    header=f"[{__get_python_filename()}: {__get_python_codeline()}lines] Warning:", 
)

if __name__ == "__main__":    
    log_msg("print only user log.")
    debug("print and save debug.log file.")
    warning("print only warning message.")