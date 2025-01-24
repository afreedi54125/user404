import logging
from telethon import events, functions, types
from Fazal import ubots, OWNER_ID, SUDO_USERS, UBOT_HNDLR

# Configure logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)

for ubot in ubots:
    @ubot.on(events.NewMessage(pattern=fr'(?i)^{UBOT_HNDLR}ban(?:\s+(\d+))?$'))
    async def ban_user(event):
        user_id = event.sender_id
        if user_id != OWNER_ID and user_id not in SUDO_USERS:
            await event.reply("❌ You don't have permission to use this command.")
            return
        
        target_user = None
        if event.is_reply:
            replied_user = await event.get_reply_message()
            if replied_user:
                target_user = replied_user.sender_id
        elif event.pattern_match.group(1):
            target_user = int(event.pattern_match.group(1))
        
        if target_user is None:
            await event.reply("❌ Please reply to a user or provide a user ID.")
            return

        chat = await event.get_chat()
        try:
            await event.client(functions.channels.EditBannedRequest(
                chat,
                target_user,
                types.ChatBannedRights(until_date=None, view_messages=True)  # Ban rights
            ))
            await event.reply(f"✅ User {target_user} has been banned.")
            logging.info(f"Banned user {target_user}.")
        except Exception as e:
            await event.reply(f"❌ Failed to ban user: {e}")

        # Delete the command message
        await event.delete()

    @ubot.on(events.NewMessage(pattern=fr'(?i)^{UBOT_HNDLR}unban(?:\s+(\d+))?$'))
    async def unban_user(event):
        user_id = event.sender_id
        if user_id != OWNER_ID and user_id not in SUDO_USERS:
            await event.reply("❌ You don't have permission to use this command.")
            return
        
        target_user = None
        if event.is_reply:
            replied_user = await event.get_reply_message()
            if replied_user:
                target_user = replied_user.sender_id
        elif event.pattern_match.group(1):
            target_user = int(event.pattern_match.group(1))
        
        if target_user is None:
            await event.reply("❌ Please reply to a user or provide a user ID.")
            return

        chat = await event.get_chat()
        try:
            await event.client(functions.channels.EditBannedRequest(
                chat,
                target_user,
                types.ChatBannedRights(until_date=None, view_messages=False)  # Remove ban rights
            ))
            await event.reply(f"✅ User {target_user} has been unbanned.")
            logging.info(f"Unbanned user {target_user}.")
        except Exception as e:
            await event.reply(f"❌ Failed to unban user: {e}")

        # Delete the command message
        await event.delete()