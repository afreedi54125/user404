import logging
from telethon import events, functions
from Fazal import ubots, OWNER_ID, SUDO_USERS

# Logging configuration
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)

# In-memory set to store blocked user IDs
blocked_users = set()

for ubot in ubots:
    @ubot.on(events.NewMessage(pattern=r'(?i)^block(?:\s|$)([\s\S]*)'))
    async def block_p_m(event):
        "To block user to direct message you."
        user_id = event.sender_id
        if user_id != OWNER_ID and user_id not in SUDO_USERS:
            await event.reply("❌ You don't have permission to use this command.")
            return

        if event.is_reply:
            replied_user = await event.get_reply_message()
            if replied_user:
                target_user_id = replied_user.sender_id
            else:
                await event.reply("❌ Reply to a message to block a user.")
                return
        else:
            target_user_id = event.pattern_match.group(1).strip()  # Get user ID from command
            try:
                target_user_id = int(target_user_id)  # Convert to int
            except ValueError:
                await event.reply("❌ Please provide a valid user ID.")
                return

        blocked_users.add(target_user_id)
        await event.client(functions.contacts.BlockRequest(target_user_id))
        await event.reply(f"🔒 User {target_user_id} has been blocked.")
        logging.info(f"User {target_user_id} blocked by {user_id}.")

    @ubot.on(events.NewMessage(pattern=r'(?i)^unblock(?:\s|$)([\s\S]*)'))
    async def unblock_pm(event):
        "To unblock a user."
        user_id = event.sender_id
        if user_id != OWNER_ID and user_id not in SUDO_USERS:
            await event.reply("❌ You don't have permission to use this command.")
            return

        if event.is_reply:
            replied_user = await event.get_reply_message()
            if replied_user:
                target_user_id = replied_user.sender_id
            else:
                await event.reply("❌ Reply to a message to unblock a user.")
                return
        else:
            target_user_id = event.pattern_match.group(1).strip()  # Get user ID from command
            try:
                target_user_id = int(target_user_id)  # Convert to int
            except ValueError:
                await event.reply("❌ Please provide a valid user ID.")
                return

        if target_user_id in blocked_users:
            blocked_users.remove(target_user_id)
            await event.client(functions.contacts.UnblockRequest(target_user_id))
            await event.reply(f"✅ User {target_user_id} has been unblocked.")
            logging.info(f"User {target_user_id} unblocked by {user_id}.")
        else:
            await event.reply("❌ User is not blocked.")