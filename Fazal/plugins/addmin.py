import logging
from telethon import events, functions, types
from Fazal import ubots, OWNER_ID, SUDO_USERS

# Configure logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)

for ubot in ubots:
    @ubot.on(events.NewMessage(pattern=r'(?i)^promote(?:\s|$)([\s\S]*)', outgoing=True))
    async def promote(event):
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
        if not chat.admin_rights and not chat.creator:
            return await event.reply("❌ You can't promote a person without admin rights.")

        try:
            await event.client(functions.channels.EditAdminRequest(
                chat,
                target_user,
                types.ChatAdminRights(
                    change_info=True,
                    post_messages=True,
                    edit_messages=True,
                    delete_messages=True,
                    invite_users=True,
                    pin_messages=True,
                    add_admins=True,
                ),
                rank=""  # Set rank to an empty string to avoid NoneType issue
            ))
            await event.reply(f"✅ User {target_user} has been promoted to admin.")
            logging.info(f"Promoted user {target_user} to admin.")
        except Exception as e:
            await event.reply(f"❌ Failed to promote user: {e}")
            
            await event.delete()

    @ubot.on(events.NewMessage(pattern=r'(?i)^demote(?:\s|$)([\s\S]*)', outgoing=True))
    async def demote(event):
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
        if not chat.admin_rights and not chat.creator:
            return await event.reply("❌ You can't demote a person without admin rights.")

        try:
            await event.client(functions.channels.EditAdminRequest(
                chat,
                target_user,
                types.ChatAdminRights(
                    change_info=False,
                    post_messages=False,
                    edit_messages=False,
                    delete_messages=False,
                    invite_users=False,
                    pin_messages=False,
                    add_admins=False,
                ),
                rank=""  # Set rank to an empty string to avoid NoneType issue
            ))
            await event.reply(f"✅ User {target_user} has been demoted from admin.")
            logging.info(f"Demoted user {target_user} from admin.")
        except Exception as e:
            await event.reply(f"❌ Failed to demote user: {e}")
            
            await event.delete()

    @ubot.on(events.NewMessage(pattern=r'(?i)^admins$', outgoing=True))
    async def list_admins(event):
        user_id = event.sender_id
        if user_id != OWNER_ID and user_id not in SUDO_USERS:
            await event.reply("❌ You don't have permission to use this command.")
            return

        chat = await event.get_chat()
        admin_list = []
        async for participant in event.client.iter_participants(chat, filter=types.ChannelParticipantsAdmins):
            admin_list.append(f"👮 Admin: {participant.first_name} (ID: {participant.id})")

        if admin_list:
            await event.reply("\n".join(admin_list))
        else:
            await event.reply("❌ No admins found in this chat.")
            
            await event.delete()