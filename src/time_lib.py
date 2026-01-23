"""
Time Formatting Library

Provides the TimeAlias class to easily generate current date and time strings in desired formats.
"""
from .core.time_lib.datetime import TimeAlias

__all__ = ["TimeAlias"]

# basic usecase
detail = TimeAlias()
date = TimeAlias(True, False)
times = TimeAlias(False, True)

# usage example
__star = TimeAlias()
__star.date_times_dist = "*"
__star.date_dist = "*"
__star.times_dist = "*"

if __name__ == "__main__":
    print(f"__star: {__star}")
    
    print(f"detail: {detail}")
    print(f"date: {date}")
    print(f"times: {times}")