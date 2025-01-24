from telethon import events, Button
from Fazal import dybot  # Ensure you're importing the bot instance
from config import UPIC, ubotversion, UPDATES_CHANNEL , OWNER_USERNAME   # Ensure this is correctly imported
from telethon import __version__
from platform import python_version

# Bot information
text = "**ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ʙᴏᴛ!**\n\n"
pm_caption = f"ᴜʙᴏᴛ ᴠᴇʀꜱɪᴏɴ `{ubotversion}`\n"
pm_caption += f"ᴘʏᴛʜᴏɴ ᴠᴇʀꜱɪᴏɴ `{python_version()}\n"
pm_caption += f"ᴛᴇʟᴇᴛʜᴏɴ ᴠᴇʀꜱɪᴏɴ `{__version__}\n"
# pm_caption += f"ᴅʏᴏʜ ᴜʙᴏᴛ ꜱᴏᴜʀᴄᴇ [ᴄʟɪᴄᴋ](https://github.com/AaghaFazal)\n\n"
pm_caption += f"ᴜʙᴏᴛ ꜱᴛᴀʀᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!"
text += pm_caption

emoji = "✨"






@dybot.on(events.NewMessage(incoming=True, pattern=r"/help"))
async def help_command(event):
    buttons = [
        [
            Button.inline("Help", b"show_help"),
            Button.inline("Commands", b"show_commands"),
        ],
        [
            Button.url("Channel", f'https://t.me/{UPDATES_CHANNEL}'),
            Button.url("Owner", f'https://t.me/{OWNER_USERNAME}'),
        ]
    ]
    
    await dybot.send_file(
        event.chat_id,
        UPIC,
        caption=text,
        buttons=buttons
    )

@dybot.on(events.CallbackQuery)
async def callback(event):
    if event.data == b"show_help":
        await event.respond("You selected: Help command. Here are the instructions...")
    elif event.data == b"show_start":
        start_page = "Welcome to the start page of the bot!"
        buttons = [[Button.inline("Back", b"show_help"), Button.inline("Main Page", b"main_page")]]
        await event.edit(start_page, buttons=buttons)
    elif event.data == b"show_settings":
        settings_page = "Here are the bot settings."
        buttons = [[Button.inline("Back", b"show_help"), Button.inline("Main Page", b"main_page")]]
        await event.edit(settings_page, buttons=buttons)
    elif event.data == b"show_commands":
        buttons = [
            [Button.inline("Spam", b"show_spam_commands"),
             Button.inline("Raid", b"show_raid_commands")],
            [Button.inline("Main Page", b"main_page")]
        ]
        await event.edit("Select a command to see details:", buttons=buttons)
    elif event.data == b"show_spam_commands":
        spam_commands_message = (
            f"{emoji} Ubot Spam Commands\n\n"
            f"{emoji}spam <count> <message to spam>\n"
            f"{emoji}spam <count> <reply to a message>\n"
            f"{emoji}spam <count> <reply to a sticker>\n"
            f"{emoji}spam <count> <reply to a video>\n"
            f"{emoji}spam <count> <reply to a GIF>\n"
            f"{emoji}spam <count> <reply to a photo>\n\n"
            f"{emoji}Count must be an integer"
        )
        buttons = [[Button.inline("Back", b"show_commands"), Button.inline("Main Page", b"main_page")]]
        await event.edit(spam_commands_message, buttons=buttons)
    elif event.data == b"show_raid_commands":
        raid_commands_message = (
            f"{emoji} Ubot Raid Commands\n\n"
            f"{emoji}raid <count> <username of User>\n"
            f"{emoji}raid <count> <reply to a User>\n\n"
            f"{emoji}replyraid <username of User>\n"
            f"{emoji}replyraid <reply to a User>\n\n"
            f"{emoji}dreplyraid <username of User>\n"
            f"{emoji}dreplyraid <reply to a User>\n\n"
            f"{emoji}Count must be an integer."
        )
        buttons = [[Button.inline("Back", b"show_commands"), Button.inline("Main Page", b"main_page")]]
        await event.edit(raid_commands_message, buttons=buttons)
    elif event.data == b"main_page":
        buttons = [
            [Button.inline("Help", b"show_help"),
             Button.inline("Commands", b"show_commands")],
            [Button.inline("Start", b"show_start"),
             Button.inline("Settings", b"show_settings")]
        ]
        await event.edit("Ubot", buttons=buttons)