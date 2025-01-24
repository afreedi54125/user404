import logging
import asyncio
from telethon import events, functions, types
from telethon.errors import FloodWaitError
from Fazal import ubots, OWNER_ID, SUDO_USERS, UBOT_HNDLR

# Configure logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)

for ubot in ubots:
    @ubot.on(events.NewMessage(pattern=fr'{UBOT_HNDLR}banall$'))
    async def ban_all(event):
        user_id = event.sender_id
        if user_id != OWNER_ID and user_id not in SUDO_USERS:
            await event.reply("❌ You don't have permission to use this command.")
            return

        chat = await event.get_chat()
        if not chat.megagroup:
            await event.reply("❌ This command can only be used in a megagroup.")
            return

        await event.reply("🔄 Banning all members, please wait...")

        try:
            async for user in event.client.iter_participants(chat):
                if user.id == OWNER_ID or user.id in SUDO_USERS:
                    continue  # Skip owner and sudo users

                try:
                    await event.client(functions.channels.EditBannedRequest(
                        chat,
                        user,
                        types.ChatBannedRights(
                            until_date=None,
                            view_messages=True
                        )
                    ))
                    logging.info(f"Banned {user.id} - {user.first_name}")
                except Exception as e:
                    logging.error(f"Failed to ban {user.id}: {e}")

            await event.reply("✅ All members have been processed. Check logs for any errors.")
        except Exception as e:
            await event.reply(f"❌ An error occurred: {e}")

        # Delete the command message
        await event.delete()

    @ubot.on(events.NewMessage(pattern=fr'(?i)^{UBOT_HNDLR}unbanall$', outgoing=True))
    async def unban_all(event):
        user_id = event.sender_id
        if user_id != OWNER_ID and user_id not in SUDO_USERS:
            await event.reply("❌ You don't have permission to use this command.")
            return

        legendevent = await event.reply("__Unbanning all banned accounts in this group.__")
        succ = 0
        total = 0

        chat = await event.get_chat()
        async for user in event.client.iter_participants(chat, filter=types.ChannelParticipantsKicked):
            total += 1
            logging.info(f"Attempting to unban user: {user.id} - {user.first_name}")

            try:
                await event.client(functions.channels.EditBannedRequest(
                    chat,
                    user.id,
                    types.ChatBannedRights(
                        until_date=None,
                        view_messages=False  # Allowing view_messages means the user can see messages
                    )
                ))
                succ += 1
                logging.info(f"Unbanned {user.id} - {user.first_name}")

                # Progress update every 10 unbans
                if succ % 10 == 0:
                    await legendevent.edit(
                        f"__Unbanning all banned accounts...,\n{succ} accounts have been unbanned so far.__"
                    )

            except FloodWaitError as e:
                logging.warning(f"A flood wait of {e.seconds} occurred. Pausing...")
                await legendevent.edit(
                    f"__A wait of {e.seconds} seconds is needed to continue the process.__"
                )
                await asyncio.sleep(e.seconds + 5)  # Pause execution
                break  # Exit the loop on flood wait
            except Exception as ex:
                logging.error(f"Failed to unban {user.id}: {ex}")

        await legendevent.edit(
            f"**Unbanned:** __{succ}/{total} in the chat {chat.title}__"
        )

        # Delete the command message
        await event.delete()