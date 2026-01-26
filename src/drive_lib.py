"""
File Utility Library

Provides abstract storage strategies and file saving utilities.
"""

import io
from .core.drive_lib.strategies import (
    DriveStrategy as _DriveStrategy,
    LocalFileStrategy,
    GoogleDriveStrategy,
    DiscordStrategy,
    TelegramStrategy,
)

__all__ = [
    "LocalFileStrategy",
    "GoogleDriveStrategy",
    "DiscordStrategy",
    "TelegramStrategy",
    "save_content",
    "load_content",
    "download_content",
]

def save_content(content: str, filename: str, strategy: _DriveStrategy = None) -> None:
    if strategy is None:
        strategy = LocalFileStrategy()
    strategy.save(io.StringIO(content), filename)

def load_content(filename: str, strategy: _DriveStrategy = None) -> str:
    if strategy is None:
        strategy = LocalFileStrategy()
    return strategy.load(filename)

def download_content(filename: str, save_path: str, strategy: _DriveStrategy = None) -> None:
    if strategy is None:
        strategy = LocalFileStrategy()
    strategy.download(filename, save_path)

if __name__ == "__main__":
    print("--- Local File Storage Test ---")
    test_content = "Hello, World! This is a test file."
    test_filename = "test_file.txt"
    
    # Save locally
    print(f"Saving '{test_filename}' locally...")
    save_content(test_content, test_filename) # Default is LocalFileStorage
    print("Saved.")

    # Load locally
    print(f"Loading '{test_filename}'...")
    loaded_content = load_content(test_filename)
    print(f"Loaded content: {loaded_content}")
    
    # Clean up
    import os
    if os.path.exists(test_filename):
        os.remove(test_filename)
        print("Test file removed.")

    print("\n--- External Storage Test (Configuration Required) ---")
    # Discord Example
    # webhook_url = "YOUR_DISCORD_WEBHOOK_URL"
    # discord_storage = DiscordStrategy(webhook_url=webhook_url)
    # save_content("Discord test content", "discord_test.txt", discord_storage)
    # print("Discord upload attempted.")

    # Telegram Example
    # bot_token = "YOUR_BOT_TOKEN"
    # chat_id = "YOUR_CHAT_ID"
    # telegram_storage = TelegramStrategy(bot_token, chat_id)
    # save_content("Telegram test content", "telegram_test.txt", telegram_storage)
    # print("Telegram upload attempted.")
