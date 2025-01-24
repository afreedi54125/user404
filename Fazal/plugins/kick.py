import logging
from telethon import functions, events
from telethon.errors import ChatAdminRequiredError, UserNotParticipantError
from Fazal import ubots, UBOT_HNDLR

# Configure logging
logging.basicConfig(level=logging.INFO)

for ubot in ubots:
    @ubot.on(events.NewMessage(pattern=fr'(?i)^{UBOT_HNDLR}kickall$', outgoing=True))
    async def kickmeall(event):
        """Command to kick all members from the group except the bot."""
        if event.is_group:
            try:
                participants = await event.client.get_participants(event.chat_id)
                total_kicked = 0
                for user in participants:
                    if user.id != event.sender_id:  # Exclude the user who initiated the command
                        try:
                            await event.client.kick_participant(event.chat_id, user.id)
                            logging.info(f"Kicked user: {user.id}")
                            total_kicked += 1
                        except UserNotParticipantError:
                            logging.warning(f"User {user.id} is not a participant.")
                        except ChatAdminRequiredError:
                            await event.reply("❌ Is action ke liye mujhe admin privileges ki zaroorat hai.")
                            return  # Exit if admin permissions are lacking
                        except Exception as e:
                            logging.error(f"Failed to kick user {user.id}: {str(e)}")
                await event.reply(f"✅ Mainne {total_kicked} members ko group se nikaal diya hai.")
            except Exception as e:
                await event.reply(f"❌ Participants ko fetch karne mein kuch galti hui: {str(e)}")
        else:
            await event.reply("❌ Yeh command sirf groups mein istemal kiya ja sakta hai.")

        # Delete the command message
        await event.delete()

    @ubot.on(events.NewMessage(pattern=fr'(?i)^{UBOT_HNDLR}kickme$', outgoing=True))
    async def kickme(event):
        """Command for the user to leave the group."""
        if event.is_group:
            await event.edit("`Nope, ye group se nikal ja raha hoon`")
            try:
                await event.client(functions.channels.LeaveChannelRequest(event.chat_id))
                await event.reply("✅ Aap group se nikal gaye hain.")
            except Exception as e:
                await event.reply(f"❌ Group se nikalne mein kuch galti hui: {str(e)}")
        else:
            await event.reply("❌ Ye command sirf groups mein istemal hoti hai.")

        # Delete the command message
        await event.delete()