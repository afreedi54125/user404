import asyncio
import logging
from telethon import events, functions, types
from Fazal import dybot, SUDO_USERS

# Set up logging
logging.basicConfig(level=logging.INFO)

async def gifspam(e, smex):
    try:
        await e.client(
            functions.messages.SaveGifRequest(
                id=types.InputDocument(
                    id=smex.media.document.id,
                    access_hash=smex.media.document.access_hash,
                    file_reference=smex.media.document.file_reference,
                ),
                unsave=True,
            )
        )
    except Exception as ex:
        logging.error(f"Error saving GIF: {ex}")

@dybot.on(events.NewMessage(incoming=True, pattern=r"/spam(?: |$)(.*)"))
async def spam(e):
    usage = ("Ubot Spam Commands\n\n"
             "`spam <count> <message to spam>`\n"
             "`spam <count> <reply to a message>`\n"
             "`spam <count> <reply to a sticker>`\n"
             "`spam <count> <reply to a video>`\n"
             "`spam <count> <reply to a GIF>`\n"
             "`spam <count> <reply to a photo>`\n\n"
             "Count must be an integer.")
    error = "UBOT"
    
    if e.sender_id not in SUDO_USERS:
        return await e.reply("You do not have permission to use this command.")

    if not e.text or len(e.text.split()) < 2:
        return await e.reply(usage)

    command_parts = e.text.split(maxsplit=1)[1].split(" ", 1)
    smex = await e.get_reply_message()

    try:
        count = int(command_parts[0])
        sleep_time = 0.02  # Reduced sleep time for faster sending

        if len(command_parts) == 2:
            message = str(command_parts[1])
            for _ in range(count):
                await e.respond(message)
                await asyncio.sleep(sleep_time)

        elif smex:
            for _ in range(count):
                if smex.media:  # Ensure the reply has media
                    if smex.media.__class__.__name__ == 'MessageMediaPhoto':
                        await e.client.send_file(e.chat_id, smex.media, caption=smex.text)
                    elif smex.media.__class__.__name__ == 'MessageMediaDocument':
                        if smex.media.document.mime_type.startswith('video'):
                            await e.client.send_file(e.chat_id, smex.media, caption=smex.text)
                        elif smex.media.document.mime_type.startswith('image/gif'):
                            await e.client.send_file(e.chat_id, smex.media, caption=smex.text)
                            await gifspam(e, smex)
                        else:
                            await e.client.send_file(e.chat_id, smex.media, caption=smex.text)
                    elif smex.media.__class__.__name__ == 'MessageMediaSticker':
                        await e.client.send_file(e.chat_id, smex.media)
                    else:
                        return await e.reply("Unsupported media type.")
                else:
                    await e.client.send_message(e.chat_id, smex.text)  # Send text if no media

                await asyncio.sleep(sleep_time)

        else:
            return await e.reply(usage)

    except ValueError:
        return await e.reply("Count must be an integer.")
    except Exception as ex:
        logging.error(f"An error occurred: {ex}")
        await e.reply("An unexpected error occurred.")