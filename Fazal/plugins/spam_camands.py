import logging
from telethon import events
from Fazal import ubots, OWNER_ID, SUDO_USERS, UBOT_HNDLR  # Ensure these imports are correct
from config import UPIC

# Logging configuration
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

emoji = "🔰"

# Spam command list
sc_list = f"""
Spam Commands:
{emoji}`{UBOT_HNDLR}spam` 
{emoji}`{UBOT_HNDLR}raid`
{emoji}`{UBOT_HNDLR}replyraid`
{emoji}`{UBOT_HNDLR}dreplyraid`
{emoji}`{UBOT_HNDLR}abuse`
{emoji}`{UBOT_HNDLR}gaali`
{emoji}`{UBOT_HNDLR}lgali`
"""

# Handler for the .sc command
for ubot in ubots:  
    @ubot.on(events.NewMessage(pattern=r'\.sc'))
    async def sc_handler(event):
        user_id = event.sender_id

        # Check if the user is authorized
        if user_id != OWNER_ID and user_id not in SUDO_USERS:
            await event.reply("❌ You don't have permission to use this command.")
            logging.warning("Unauthorized access attempt by user_id: %s", user_id)
            return

        logging.info("Received .sc command.")
        
        # Send the UPIC file with the command list as the caption
        await event.client.send_file(
            event.chat_id,
            UPIC,
            caption=sc_list  # Use caption to add command list
        )
        
        logging.info("Sent sc message with UPIC and command list.")
