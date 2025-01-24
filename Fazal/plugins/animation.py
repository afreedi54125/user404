import asyncio
from collections import deque
from telethon import events  # Import events from Telethon
from Fazal import ubots, OWNER_ID, SUDO_USERS, UBOT_HNDLR

menu_category = "fun"

# Define the eor function
async def eor(event, text):
    # Check if the text to be sent is different from the current message
    if event.raw_text != text:
        return await event.edit(text)
    return event  # Return the event if no edit is necessary

for ubot in ubots:
    @ubot.on(events.NewMessage(pattern=fr"^{UBOT_HNDLR}lol$"))
    async def lol(event):
        "Animation command"
        event = await eor(event, "lol")
        deq = deque("😂🤣😂🤣😂🤣")
        for _ in range(48):
            await asyncio.sleep(0.2)
            new_text = "".join(deq)
            if event.raw_text != new_text:
                await event.edit(new_text)
            deq.rotate(1)
        await event.delete()  # Delete the command message

    @ubot.on(events.NewMessage(pattern=fr"^{UBOT_HNDLR}nothappy$"))
    async def nothappy(event):
        "Animation command"
        event = await eor(event, "nothappy")
        deq = deque("😁☹️😁☹️😁☹️😁")
        for _ in range(48):
            await asyncio.sleep(0.2)
            new_text = "".join(deq)
            if event.raw_text != new_text:
                await event.edit(new_text)
            deq.rotate(1)
        await event.delete()  # Delete the command message

    @ubot.on(events.NewMessage(pattern=fr"^{UBOT_HNDLR}muah$"))
    async def muah(event):
        "Animation command"
        event = await eor(event, "muah")
        deq = deque("😗😙😚😚😘")
        for _ in range(48):
            await asyncio.sleep(0.2)
            new_text = "".join(deq)
            if event.raw_text != new_text:
                await event.edit(new_text)
            deq.rotate(1)
        await event.delete()  # Delete the command message

    @ubot.on(events.NewMessage(pattern=fr"^{UBOT_HNDLR}heart$"))
    async def heart(event):
        "Animation command"
        event = await eor(event, "heart")
        deq = deque("❤️🧡💛💚💙💜🖤")
        for _ in range(48):
            await asyncio.sleep(0.2)
            new_text = "".join(deq)
            if event.raw_text != new_text:
                await event.edit(new_text)
            deq.rotate(1)
        await event.delete()  # Delete the command message

    @ubot.on(events.NewMessage(pattern=fr"^{UBOT_HNDLR}gym$"))
    async def gym(event):
        "Animation command"
        event = await eor(event, "gym")
        deq = deque("🏃‍🏋‍🤸‍🏃‍🏋‍🤸‍🏃‍🏋‍🤸‍")
        for _ in range(48):
            await asyncio.sleep(0.2)
            new_text = "".join(deq)
            if event.raw_text != new_text:
                await event.edit(new_text)
            deq.rotate(1)
        await event.delete()  # Delete the command message