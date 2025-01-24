import logging
from telethon import events, functions, types
from Fazal import ubots, OWNER_ID, SUDO_USERS, UBOT_HNDLR

# Configure logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)

MUTE_RIGHTS = types.ChatBannedRights(until_date=None, send_messages=True)

for ubot in ubots:
    @ubot.on(events.NewMessage(pattern=fr'(?i)^{UBOT_HNDLR}mute(?:\s|$)([\s\S]*)', outgoing=True))
    async def mute(event):
        user_id = event.sender_id
        if user_id != OWNER_ID and user_id not in SUDO_USERS:
            await event.reply("❌ You don't have permission to use this command.")
            return

        # Get target user
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
        admin_rights = chat.admin_rights

        if not admin_rights and not chat.creator:
            return await event.reply("❌ You can't mute a person without admin rights.")

        if target_user == OWNER_ID:
            return await event.reply("❌ You can't mute yourself.")

        # Check if user is already muted
        try:
            permissions = await event.client(functions.channels.GetParticipantRequest(chat, target_user))
            if permissions.participant.banned_rights.send_messages:
                return await event.reply("❌ This user is already muted.")
        except Exception as e:
            if "UserNotParticipant" in str(e):
                return await event.reply("❌ This user is not in the chat.")

        # Mute the user
        try:
            await event.client(functions.channels.EditBannedRequest(
                chat,
                target_user,
                MUTE_RIGHTS
            ))
            await event.reply(f"✅ User {target_user} has been muted.")
            logging.info(f"Muted user {target_user}.")
        except Exception as e:
            await event.reply(f"❌ Failed to mute user: {e}")

        # Delete the command message
        await event.delete()

    @ubot.on(events.NewMessage(pattern=fr'(?i)^{UBOT_HNDLR}unmute(?:\s|$)([\s\S]*)', outgoing=True))
    async def unmute(event):
        user_id = event.sender_id
        if user_id != OWNER_ID and user_id not in SUDO_USERS:
            await event.reply("❌ You don't have permission to use this command.")
            return

        # Get target user
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

        # Unmute the user
        try:
            await event.client(functions.channels.EditBannedRequest(
                chat,
                target_user,
                types.ChatBannedRights(until_date=None, send_messages=False)
            ))
            await event.reply(f"✅ User {target_user} has been unmuted.")
            logging.info(f"Unmuted user {target_user}.")
        except Exception as e:
            await event.reply(f"❌ Failed to unmute user: {e}")

        # Delete the command message
        await event.delete()