from telethon import events, Button
from Fazal import dybot  # Ensure you're importing the bot instance
from config import STARTPIC, ubotversion, UPDATES_CHANNEL , OWNER_USERNAME  # Ensure this is correctly imported
from telethon import __version__
from platform import python_version

@dybot.on(events.NewMessage(incoming=True, pattern=r"/start"))
async def start(event):
    # Customize the welcome message
    text = "**ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ʙᴏᴛ!**\n\n"
    pm_caption = f"ᴜʙᴏᴛ ᴠᴇʀꜱɪᴏɴ `{ubotversion}`\n"
    pm_caption += f"ᴘʏᴛʜᴏɴ ᴠᴇʀꜱɪᴏɴ `{python_version()}`\n"
    pm_caption += f"ᴛᴇʟᴇᴛʜᴏɴ ᴠᴇʀꜱɪᴏɴ `{__version__}`\n"
    # pm_caption += f"ᴜʙᴏᴛ ꜱᴏᴜʀᴄᴇ [ᴄʟɪᴄᴋ](https://github.com/AaghaFazal)\n\n"
    text += pm_caption

    # Create buttons
    buttons = [
    [Button.url("Owner", f'https://t.me/{OWNER_USERNAME}'), Button.url("Channel", f'https://t.me/{UPDATES_CHANNEL}')]
]
    
    # Send the message with buttons
    await dybot.send_file(
        event.chat_id,
        STARTPIC,
        caption=text,
        buttons=buttons
    )

