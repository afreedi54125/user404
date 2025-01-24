import logging
import asyncio
from telethon import events, types
from Fazal import ubots, OWNER_ID, SUDO_USERS, UBOT_HNDLR

# Setting up logging
logging.basicConfig(level=logging.INFO)

for ubot in ubots:
    @ubot.on(events.NewMessage(pattern=f'^{UBOT_HNDLR}spam (\\d+) ?(.*)'))
    async def repeat_message(event):
        # Check if the user is either the OWNER or in the SUDO_USERS list
        if event.sender_id != OWNER_ID and event.sender_id not in SUDO_USERS:
            await event.respond("You are not authorized to use this command.")
            return

        count = int(event.pattern_match.group(1))
        message_to_repeat = event.pattern_match.group(2)

        # Check if the command has a specific message or if it's a reply
        if not message_to_repeat and event.is_reply:
            replied_message = await event.get_reply_message()  # Get the replied message

            if replied_message.text:  # For text messages
                message_to_repeat = replied_message.text
            elif replied_message.media:  # Check the type of media
                media = replied_message.media

                if isinstance(media, types.MessageMediaPhoto):
                    message_to_repeat = media  # Photo
                elif isinstance(media, types.MessageMediaDocument):
                    mime_type = media.document.mime_type

                    # Check for stickers
                    if mime_type == 'image/webp':
                        message_to_repeat = media  # Sticker
                    # Check for GIFs
                    elif mime_type in ['video/mp4', 'video/x-gif', 'image/gif']:
                        message_to_repeat = media  # GIF
                    # Check for videos
                    elif mime_type.startswith('video/'):
                        message_to_repeat = media  # Video
                    else:
                        await event.respond("Unsupported media type.")
                        return

        elif not message_to_repeat:
            await event.respond("Please provide a message or reply to a message.")
            return

        for _ in range(count):
            if isinstance(message_to_repeat, str):  # If it's a text message
                await event.respond(message_to_repeat)
            elif isinstance(message_to_repeat, types.MessageMediaPhoto):  # For photo
                await event.reply(file=await event.client.download_media(message_to_repeat))
            elif hasattr(message_to_repeat, 'video'):  # For video
                await event.reply(file=await event.client.download_media(message_to_repeat))  # Sending the video
            elif isinstance(message_to_repeat, types.MessageMediaDocument):  # For stickers/GIFs
                await event.reply(file=await event.client.download_media(message_to_repeat))  # Sending sticker or GIF
            else:
                await event.respond("Unsupported media type.")

            await asyncio.sleep(1)  # Optional: wait 1 second between messages

        # Delete the command message
        await event.delete()