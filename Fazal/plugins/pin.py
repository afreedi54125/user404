import logging
from telethon import events, functions, types
from Fazal import ubots, OWNER_ID, SUDO_USERS, UBOT_HNDLR

# Configure logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)

for ubot in ubots:
    @ubot.on(events.NewMessage(pattern=fr'(?i)^{UBOT_HNDLR}pin(?:\s|$)', outgoing=True))
    async def pin(event):
        user_id = event.sender_id
        if user_id != OWNER_ID and user_id not in SUDO_USERS:
            await event.reply("❌ You don't have permission to use this command.")
            return

        if not event.is_reply:
            await event.reply("❌ Please reply to a message to pin it.")
            return

        replied_message = await event.get_reply_message()
        chat = await event.get_chat()

        if not (chat.admin_rights and chat.admin_rights.pin_messages) and not chat.creator:
            await event.reply("❌ You can't pin messages without admin rights.")
            return

        try:
            await event.client(functions.messages.UpdatePinnedMessageRequest(
                peer=chat,
                id=replied_message.id,
                silent=False  # Set to True if you want to pin silently
            ))
            await event.reply("✅ Message pinned successfully.")
            logging.info(f"Message pinned in chat: {chat.title}")
        except Exception as e:
            await event.reply(f"❌ Failed to pin message: {e}")

        # Delete the command message
        await event.delete()

    @ubot.on(events.NewMessage(pattern=fr'(?i)^{UBOT_HNDLR}unpin(?:\s|$)([\s\S]*)', outgoing=True))
    async def unpin(event):
        user_id = event.sender_id
        if user_id != OWNER_ID and user_id not in SUDO_USERS:
            await event.reply("❌ You don't have permission to use this command.")
            return

        chat = await event.get_chat()

        if not chat.admin_rights and not chat.creator:
            await event.reply("❌ You can't unpin messages without admin rights.")
            return

        try:
            await event.client(functions.messages.UnpinAllMessagesRequest(chat))
            await event.reply("✅ All pinned messages have been unpinned.")
            logging.info(f"All messages unpinned in chat: {chat.title}")
        except Exception as e:
            await event.reply(f"❌ Failed to unpin messages: {e}")

        # Delete the command message
        await event.delete()