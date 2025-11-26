import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))) # module path set

from src.module.printer import log_msg

log_msg("Utility 'use_modules' set up successfully.")