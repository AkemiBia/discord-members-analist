# Discord Member Analysis Bot

This is a Discord bot that allows you to analyze, save, and update member information from a server in a SQLite database. It provides commands to view member profiles and allows users to set their own bios.

## Features

- **Member Analysis**: The bot can analyze all server members and save their information to the SQLite database, including name, nickname, avatar, status, activity, roles, join date, creation date, and bio.
- **Member Profile**: Users can view saved profiles, including information such as status, activity, roles, join date, and bio.
- **Set Bio**: Users can set or update their bio using a command.
- **Auto-save New Members**: When a new member joins the server, their information is automatically saved to the database.

## Commands

### `!analyze`

This command allows the bot to analyze all server members and save their information to the SQLite database.

**Example Usage**:
!analyze

### `!set_bio <bio>`

This command lets members set or update their bio.

**Example Usage**:
!set_bio I am a developer!

### `!profile [member]`

This command shows the profile of the specified member or the author's profile if no member is provided. It displays information like name, nickname, status, activity, roles, join date, creation date, and bio.

**Example Usage**:
!profile @Ieren

## Dependencies

- **discord.py**: Python library to interact with the Discord API.
- **sqlite3**: Standard Python library to interact with SQLite databases.

### How to Install

1. Clone this repository or download the code.
2. Install the required dependencies:
    ```bash
    pip install discord.py
    ```

3. Replace the bot token in the code with your own Discord bot token:
    ```python
    bot.run("YOUR_BOT_TOKEN_HERE")
    ```
