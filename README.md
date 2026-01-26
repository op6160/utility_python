
# Python Utility Library

## Overview

This repository contains a collection of Python utility modules designed to simplify common tasks and provide robust solutions for various programming needs. The library includes modules for browser automation, flexible file storage, logging, OS and Python runtime introspection, time formatting, and text manipulation.

## Features

### Browser Automation (`browser_lib`)

Provides high-level browser automation capabilities using Selenium. It includes features to bypass common anti-bot detection mechanisms.

- **`get_html_content(url, load_time)`**: Fetches and returns the full HTML content of a given URL after the page has loaded.
- **`save_mhtml(url, filename, strategy, load_time)`**: Captures a complete webpage snapshot in MHTML format and saves it using a specified storage strategy.
- **`load_mhtml(filename, strategy)`**: Loads MHTML content from a file.
- **Anti-Bot Evasion**: The underlying WebDriver is configured with several options to appear like a regular user, including:
  - Randomized User-Agents.
  - Disabling of automation-related JavaScript flags (`navigator.webdriver`).
  - Standard screen resolution settings.

### File Storage (`drive_lib`)

Offers a flexible and extensible file storage system using a strategy pattern. This allows you to save, load, and download content from various local or cloud-based storage backends.

- **`save_content(content, filename, strategy)`**: Saves string content to a file using the specified strategy.
- **`load_content(filename, strategy)`**: Loads content from a file as a string using the specified strategy.
- **`download_content(filename, save_path, strategy)`**: Downloads a file from the storage to a local path.

**Available Strategies (`core.drive_lib.strategies`):**

- **`LocalFileStrategy`**: The default strategy. Saves files to the local filesystem.
- **`GoogleDriveStrategy`**: Uploads and downloads files to/from a specific Google Drive folder. Requires Google API credentials. It can dynamically install the required `google-api-python-client` library if not present.
- **`DiscordStrategy`**: Uses a Discord channel for file storage. Can upload via a bot token (allowing for searching) or a webhook URL. Loading requires a bot token to search channel history.
- **`TelegramStrategy`**: Uploads files to a Telegram chat or channel via a bot token. Due to limitations in the Telegram Bot API, searching and loading files by name is not supported.

### Logging (`logger_lib`)

A versatile logging module for both console and file-based logging.

- **`log_msg`**: A simple logger for printing messages to the console with a timestamp.
- **`debug`**: A logger that prints messages to the console and also appends them to a `logs/debug.log` file.
- **`warning`**: A logger that displays a warning message, including the filename and line number where it was called.
- **`MessageFormatter`**: A powerful, callable class that allows you to create your own custom loggers with specific headers, footers, and file output paths.

### OS Utilities (`os_lib`)

A set of functions to inspect the host operating system and shell environment.

- **`get_os_type()`**: Returns the current OS (`"windows"`, `"linux"`, `"mac"`).
- **`get_shell_type()`**: Returns the current shell (`"zsh"`, `"bash"`, `"powershell"`).
- **`get_shell_profile()`**: Determines the path to the appropriate shell profile file (e.g., `.zshrc`, `.bashrc`, or PowerShell's `$PROFILE`).

### Python Runtime (`py_lib`)

Utilities for introspecting the Python execution environment.

- **`get_python_filename()`**: Returns the basename of the file from which it is called.
- **`get_python_codeline()`**: Returns the line number from which it is called.
- **`install_lib(lib_name, install_name)`**: Checks if a library is installed and, if not, attempts to install it via `pip`.

### Time Utilities (`time_lib`)

Provides a convenient way to format dates and times.

- **`TimeAlias` class**: A class to generate formatted date and time strings. You can customize the delimiters for date, time, and the separator between them.
- **Pre-configured instances**:
    - `detail`: Outputs the full date and time (e.g., `2026-01-26 14:00:00`).
    - `date`: Outputs the date only (e.g., `2026-01-26`).
    - `times`: Outputs the time only (e.g., `14:00:00`).

## Installation

To use this library, clone the repository and install the required dependencies.

```bash
git clone <repository-url>
cd utility_python
pip install -r requirements.txt
```
If you intend to use development tools, install the development requirements as well:
```bash
pip install -r requirements.txt.dev
```

## Usage

Here are some basic examples of how to use the modules in this library.

**Browser Automation:**

```python
from src.browser_lib import get_html_content, save_mhtml

# Get the HTML of a page
html = get_html_content("https://example.com")
print(html[:500])

# Save a webpage as an MHTML file locally
save_mhtml("https://example.com", "example.mhtml")
```

**File Storage:**

```python
from src.drive_lib import save_content, load_content, LocalFileStrategy

# Use the default local storage
save_content("This is a test.", "my_file.txt")
content = load_content("my_file.txt")
print(content)

# The LocalFileStrategy is used by default, but you can be explicit
local_strategy = LocalFileStrategy(base_path="data")
save_content("Another test.", "my_other_file.txt", strategy=local_strategy)
```

**Logging:**

```python
from src.logger_lib import log_msg, debug, warning

log_msg("This is an informational message.")
debug("This is a debug message. It will be saved to logs/debug.log.")
warning("This is a warning.")
```

**Time Formatting:**

```python
from src.time_lib import detail, date, times

print(f"Detail: {detail}")
print(f"Date only: {date}")
print(f"Time only: {times}")
```
