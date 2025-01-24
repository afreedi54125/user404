import logging
from telethon import events
from telethon import __version__  # Import the version from Telethon
from Fazal import ubots, OWNER_ID, SUDO_USERS, UBOT_HNDLR
from config import UPIC
from platform import python_version
import time

# Logging configuration
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

# Define necessary variables
my = "ᴜʙᴏᴛ ɪꜱ ᴀʟɪᴠᴇ"
emoji = "🔰"
ubotversion = "1.0"
uptime = str(time.time())
IPIC = UPIC

ubot_caption = (
    f"**{my}**\n\n"
    f"**{emoji} ᴛᴇʟᴇᴛʜᴏɴ ᴠᴇʀꜱɪᴏɴ ** `{__version__}`\n"
    f"**{emoji} ᴜʙᴏᴛ ᴠᴇʀꜱɪᴏɴ ** `{ubotversion}`\n"
    f"**{emoji} ᴘʏᴛʜᴏɴ ᴠᴇʀꜱɪᴏɴ ** `{python_version()}`\n"
    # f"**{emoji} ᴜʙᴏᴛ ꜱᴏᴜʀᴄᴇ [ᴄʟɪᴄᴋ](https://github.com/AaghaFazal)**\n"
    f"**{emoji} ᴜʙᴏᴛ ᴄʜᴀɴɴᴇʟ [ᴄʟɪᴄᴋ](https://t.me/TheLgcyDev)**\n"
    f"{emoji} ᴜʙᴏᴛ ᴏᴡɴᴇʀ [ᴄʟɪᴄᴋ](https://t.me/LGCY_OFFICIAL)\n\n"
)

for ubot in ubots:  # Use 'ubots' as the list of bot instances
    @ubot.on(events.NewMessage(pattern=fr'^{UBOT_HNDLR}alive$'))
    async def alive_handler(event):
        try:
            user_id = event.sender_id
            logging.info("Received .alive command from user_id: %s", user_id)

            if user_id == OWNER_ID or user_id in SUDO_USERS:
                logging.info("User is authorized.")
                await event.client.send_file(
                    event.chat_id,
                    IPIC,
                    caption=ubot_caption
                )
                logging.info("Sent alive message to user_id: %s", user_id)
            else:
                logging.warning("Unauthorized access attempt by user_id: %s", user_id)
                await event.reply("You don't have permission to use this command.")

            # Delete the command message
            await event.delete()

        except Exception as e:
            logging.error("Error in .alive handler: %s", e)
