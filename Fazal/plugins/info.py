import logging
from telethon import events, functions, types
from Fazal import ubots, OWNER_ID, SUDO_USERS, UBOT_HNDLR

# Configure logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)

for ubot in ubots:
    @ubot.on(events.NewMessage(pattern=fr'(?i)^{UBOT_HNDLR}info(?:\s@)?([\w\.\-]+)?$', outgoing=True))
    async def info(event):
        user_id = event.sender_id

        # Check if the command is a reply or if a username is provided
        if event.is_reply:
            target_message = await event.get_reply_message()
            target_user = target_message.sender if target_message else None
        else:
            username = event.pattern_match.group(1)
            if username:
                try:
                    target_user = await event.client.get_entity(username)
                except Exception as e:
                    await event.reply(f"❌ User not found: {e}")
                    return
            else:
                await event.reply("❌ Please reply to a message or provide a username.")
                return

        if not target_user:
            await event.reply("❌ Unable to retrieve user information.")
            return
        
        # Prepare response message
        response = f"**User Information:**\n"
        
        # Check for profile photo
        photo_path = None
        if target_user.photo:
            photos = await event.client.get_profile_photos(target_user, limit=1)
            if photos:
                # Get the path for the first photo
                photo_path = await event.client.download_profile_photo(photos[0])
                response += f"**Profile Photo:** [Click Here](attachment://photo)\n"
            else:
                response += "**Profile Photo:** No photo available.\n"
        else:
            response += "**Profile Photo:** No photo available.\n"

        response += f"**Name:** {target_user.first_name} {target_user.last_name or ''}\n"
        response += f"**Username:** @{target_user.username or 'No username'}\n"
        response += f"**User ID:** {target_user.id}\n"

        # Check if the target is a group/channel and provide additional details if applicable
        if isinstance(target_user, (types.Channel, types.Chat)):
            response += f"**Members:** {target_user.participants_count}\n"
            response += f"**Description:** {getattr(target_user, 'about', 'No description')}\n"

        await event.reply(response, file=photo_path if photo_path else None)

        # Log the info command usage
        logging.info(f"Info command used by {user_id} for user {target_user.id}.")

        # Delete the command message
        await event.delete()