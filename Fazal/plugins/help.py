import logging
from telethon import events
from Fazal import ubots, OWNER_ID, SUDO_USERS, UBOT_HNDLR  # Ensure these imports are correct
from config import UPIC
# Logging configuration
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)
emoji = "🔰"


commands_list = f"""
Available Commands:
{emoji}`{UBOT_HNDLR}alive`
{emoji}`{UBOT_HNDLR}add`
{emoji}`{UBOT_HNDLR}inviteall`
{emoji}`{UBOT_HNDLR}promote`
{emoji}`{UBOT_HNDLR}demote`
{emoji}`{UBOT_HNDLR}admins`
{emoji}`{UBOT_HNDLR}ban`
{emoji}`{UBOT_HNDLR}unban`
{emoji}`{UBOT_HNDLR}banall`
{emoji}`{UBOT_HNDLR}unbanall`
{emoji}`{UBOT_HNDLR}kickall`
{emoji}`{UBOT_HNDLR}kickme`
{emoji}`{UBOT_HNDLR}mute`
{emoji}`{UBOT_HNDLR}unmute`
{emoji}`{UBOT_HNDLR}pin`
{emoji}`{UBOT_HNDLR}unpin`
{emoji}`{UBOT_HNDLR}join`
{emoji}`{UBOT_HNDLR}leave`
{emoji}`{UBOT_HNDLR}info`
{emoji}`{UBOT_HNDLR}block`
{emoji}`{UBOT_HNDLR}unblock`
"""

for ubot in ubots:  
    @ubot.on(events.NewMessage(pattern=r'\.help'))
    async def help_handler(event):
        user_id = event.sender_id

        # Check if the user is authorized
        if user_id != OWNER_ID and user_id not in SUDO_USERS:
            await event.reply("❌ You don't have permission to use this command.")
            logging.warning("Unauthorized access attempt by user_id: %s", user_id)
            return

        logging.info("Received .help command.")
        await event.client.send_file(
            event.chat_id,
            UPIC,
            caption=commands_list  # Use caption to add command list
        )
        logging.info("Sent help message.")