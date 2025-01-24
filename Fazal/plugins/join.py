import logging
from telethon import events, functions
from telethon.errors import UserNotParticipantError, ChannelPrivateError, ChatAdminRequiredError
from Fazal import ubots, OWNER_ID, SUDO_USERS, UBOT_HNDLR  # Ensure these are defined

# Logging configuration
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

# Function to check if the user is authorized
def is_authorized(user_id):
    return user_id == OWNER_ID or user_id in SUDO_USERS

# Command to add a user to the group
for ubot in ubots:

    @ubot.on(events.NewMessage(pattern=fr'(?i)^{UBOT_HNDLR}join (\S+)'))
    async def join_channel(event):
        if not is_authorized(event.sender_id):
            return

        channel_username = event.pattern_match.group(1).strip()
        joining_message = await event.reply("Joining...")

        try:
            channel = await ubot.get_entity(channel_username)
            me = await ubot.get_me()

            # Check if the bot is already a member of the channel
            try:
                await ubot(functions.channels.GetParticipantRequest(channel, me.id))
                await joining_message.delete()
                await event.reply("The bot is already a member of this channel.")
                return
            except (UserNotParticipantError, ChannelPrivateError):
                pass  # Not a member, proceed to join

            # Attempt to join the channel
            await ubot(functions.channels.JoinChannelRequest(channel))
            await joining_message.delete()
            await event.reply("Joined successfully.")
        except ChatAdminRequiredError:
            await joining_message.delete()
            await event.reply("Error: The bot needs to be an admin to join this channel.")
        except Exception as e:
            await joining_message.delete()
            await event.reply(f"An error occurred: {str(e)}")
        finally:
            await event.delete()  # Delete the command message

    @ubot.on(events.NewMessage(pattern=fr'(?i)^{UBOT_HNDLR}leave (\S+)'))
    async def exit_channel(event):
        if not is_authorized(event.sender_id):
            return

        channel_username = event.pattern_match.group(1).strip()
        leaving_message = await event.reply("Leaving...")

        try:
            channel = await ubot.get_entity(channel_username)
            me = await ubot.get_me()

            # Check if the bot is a member of the channel
            try:
                await ubot(functions.channels.GetParticipantRequest(channel, me.id))
            except UserNotParticipantError:
                await leaving_message.delete()
                await event.reply("The bot is not a member of this channel.")
                return

            # Attempt to leave the channel
            await ubot(functions.channels.LeaveChannelRequest(channel))
            await leaving_message.delete()
            await event.reply("Left the channel successfully.")
        except Exception as e:
            await leaving_message.delete()
            await event.reply(f"An error occurred: {str(e)}")
        finally:
            await event.delete()  # Delete the command message