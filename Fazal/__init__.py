import logging
from telethon import TelegramClient
from telethon.sessions import StringSession
from config import CMD_HNDLR, UBOT_HNDLR, API_ID, API_HASH, BOT_TOKEN, GROUP_ID, SUDO_USERS, OWNER_ID, STRING_SESSION

# Set up logging
logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.INFO
)

# Initialize the main bot
ubots = [
    TelegramClient(StringSession(session), API_ID, API_HASH, auto_reconnect=True)
    for session in STRING_SESSION
]
dybot = TelegramClient("dybot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Initialize the telebot instance with the first token

# If you want to keep multiple bots for other functionalities, you can store them in a list.
# For now, we will use only one for the command handling.
logging.info("[INFO] Successfully started all bot clients. Now loading plugins!")

# Here you can load your plugins or additional functionality
# Example: load_all_plugins() or similar function


# Example usage of group and sudo users
logging.info(f"Group ID: {GROUP_ID}")
logging.info(f"SUDO Users: {SUDO_USERS}")
logging.info(f"OWNER ID: {OWNER_ID}")