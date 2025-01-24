import asyncio
import random        
from telethon import events
from resources.data import RAID, REPLYRAID
from Fazal import dybot, OWNER_ID, SUDO_USERS, CMD_HNDLR  

que = {}

hl = CMD_HNDLR  # Set command handler here

@dybot.on(events.NewMessage(incoming=True, pattern=r"\%sraid(?: |$)(.*)" % hl))
async def raid_handler(e):
    usage = "Ubot Raid Commands\n\nCommand:\n\n.raid <count> <Username of User>\n\n.raid <count> <reply to a User>\n"
    
    if e.sender_id in SUDO_USERS:
        if e.text[0].isalpha() and e.text[0] in ("/", "#", "@", "!"):
            return await e.reply(usage)
        
        command_parts = e.text.split(maxsplit=1)
        if len(command_parts) > 1:
            count_and_user = command_parts[1].split(" ", 1)
            
            if len(count_and_user) == 2:
                user = str(count_and_user[1])
                a = await e.client.get_entity(user)
                g = a.id
                
                if g == OWNER_ID or g in SUDO_USERS:
                    return await e.reply("Cannot raid this user.")
                
                c = a.first_name
                username = f"[{c}](tg://user?id={g})"
                counter = int(count_and_user[0])
                for _ in range(counter):
                    reply = random.choice(RAID)
                    caption = f"{username} {reply}"
                    async with e.client.action(e.chat_id, "typing"):
                        await e.client.send_message(e.chat_id, caption)
                        await asyncio.sleep(0.5)
        
            elif e.reply_to_msg_id:             
                a = await e.get_reply_message()
                b = await e.client.get_entity(a.sender_id)
                g = b.id
                
                if g == OWNER_ID or g in SUDO_USERS:
                    return await e.reply("Cannot raid this user.")
                
                c = b.first_name
                counter = int(count_and_user[0])
                username = f"[{c}](tg://user?id={g})"
                for _ in range(counter):
                    reply = random.choice(RAID)
                    caption = f"{username} {reply}"
                    async with e.client.action(e.chat_id, "typing"):
                        await e.client.send_message(e.chat_id, caption)
                        await asyncio.sleep(0.3)
        else:
            await e.reply(usage)

@dybot.on(events.NewMessage(incoming=True, pattern=r"\%sreplyraid(?: |$)(.*)" % hl))
async def reply_raid_handler(e):
    usage = "Replyraid Commands\n\nCommand:\n\n.replyraid <Username of User>\n\n.replyraid <reply to a User>."
    
    if e.sender_id in SUDO_USERS:
        command_parts = e.text.split(maxsplit=1)
        
        if len(command_parts) > 1:
            message = str(command_parts[1])
            a = await e.client.get_entity(message)
            user_id = a.id
            
            if user_id == OWNER_ID or user_id in SUDO_USERS:
                return await e.reply("Cannot reply raid this user.")
            
            que[user_id] = []
            await e.reply("Activated replyraid for user.")
        
        elif e.reply_to_msg_id:             
            a = await e.get_reply_message()
            umser = await e.client.get_entity(a.sender_id)
            user_id = umser.id
            
            if user_id == OWNER_ID or user_id in SUDO_USERS:
                return await e.reply("Cannot reply raid this user.")
            
            que[user_id] = []
            await e.reply("Activated replyraid for replied user.")
        else:
            await e.reply(usage)

@dybot.on(events.NewMessage(incoming=True, pattern=r"\%sdreplyraid(?: |$)(.*)" % hl))
async def deactivate_reply_raid_handler(e):
    usage = "Dreplyraid Commands\n\nCommand:\n\n.dreplyraid <Username of User>\n\n.dreplyraid <reply to a User>"
    
    if e.sender_id in SUDO_USERS:
        command_parts = e.text.split(maxsplit=1)
        
        if len(command_parts) > 1:
            message = str(command_parts[1])
            a = await e.client.get_entity(message)
            user_id = a.id
            
            if user_id in que:
                que.pop(user_id)
                await e.reply("De-Activated Reply Raid for user.")
            else:
                await e.reply("No active reply raid for this user.")
        
        elif e.reply_to_msg_id:             
            a = await e.get_reply_message()
            b = await e.client.get_entity(a.sender_id)
            user_id = b.id
            
            if user_id in que:
                que.pop(user_id)
                await e.reply("De-Activated Reply Raid for replied user.")
            else:
                await e.reply("No active reply raid for this user.")
        else:
            await e.reply(usage)

@dybot.on(events.NewMessage(incoming=True))
async def reply_message_handler(event):
    global que
    user_id = event.sender_id
    
    if user_id not in que:
        return  # Exit if the user is not in the queue
    
    async with event.client.action(event.chat_id, "typing"):
        await asyncio.sleep(0.2)

    if REPLYRAID:  # Check if REPLYRAID is not empty
        reply_message = random.choice(REPLYRAID)
        await event.client.send_message(
            entity=event.chat_id,
            message=reply_message,
            reply_to=event.message.id,
        )
    else:
        print("REPLYRAID is empty.")  # Debug message