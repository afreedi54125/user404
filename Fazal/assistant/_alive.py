import os
from Fazal import dybot, OWNER_ID, SUDO_USERS, CMD_HNDLR
from telethon.tl.functions.users import GetFullUserRequest
from telethon import events, version, Button
from config import UPIC

CAPTION = "Ubot Assistant is alive\n\n"
CAPTION += f"**Python Version** : `3.10.1`\n"
CAPTION += f"**Telethon Version** : `{version.__version__}`\n"
CAPTION += f"**Ubot version**  : `1.0`\n"

@dybot.on(events.NewMessage(incoming=True, pattern=f"{CMD_HNDLR}alive(?: |$)(.*)"))
async def alive(event):
    print("Command triggered by:", event.sender_id)  # Debug statement
    if event.sender_id in SUDO_USERS:
        print("User is a SUDO user.")  # Debug statement
        if UPIC:  # Check if UPIC is defined
            print("UPIC URL:", UPIC)  # Debug statement
            try:
                await dybot.send_file(event.chat_id,
                                      UPIC,
                                      caption=CAPTION,
                                      buttons=[
                    [
                        Button.url("channel", "https://t.me/TheLgcyDev"),
                        Button.url("group", "https://t.me/LGCY_OFFICIAL")
                    ],
                    [
                        Button.url("Owner", "https://t.me/AaghaFazal")
                    ]
                ])
                print("File sent successfully.")  # Debug statement
            except Exception as e:
                print(f"Error sending file: {e}")  # Log the error
                await event.reply("Failed to send file.")
        else:
            await event.reply("Error: Picture URL not defined.")
    else:
        await event.reply("You are not authorized to use this command.")

async def get_user(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        replied_user = await event.client(GetFullUserRequest(previous_message.sender_id))
        return replied_user.user.id
    return None