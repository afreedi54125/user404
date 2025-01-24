import logging
from telethon import events, functions
from Fazal import ubots, OWNER_ID, SUDO_USERS, UBOT_HNDLR  # Ensure these are defined
import asyncio

# Logging configuration
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

# Command to add a user to the group
for ubot in ubots:
    @ubot.on(events.NewMessage(pattern=fr'(?i)^{UBOT_HNDLR}add (.*)'))
    async def add_handler(event):
        user_id = event.sender_id

        # Check if the user is authorized
        if user_id != OWNER_ID and user_id not in SUDO_USERS:
            await event.reply("❌ You don't have permission to use this command.")
            logging.warning("Unauthorized access attempt by user_id: %s", user_id)
            return

        username = event.pattern_match.group(1)
        try:
            user = await event.client.get_entity(username)
            if user:
                # Attempt to add the user to the group
                try:
                    await event.client(functions.channels.InviteToChannelRequest(
                        event.chat_id,
                        [user]
                    ))
                    await event.reply(f"✅ Successfully added {user.first_name} to the group.")
                    logging.info(f"Added {user.first_name} to the group.")
                except Exception as e:
                    # Check for privacy issues
                    if 'You have no access' in str(e):
                        await event.reply(f"❌ Cannot add {user.first_name}: Privacy settings prevent this.")
                    else:
                        await event.reply(f"❌ Failed to add {user.first_name}: {e}")
            else:
                await event.reply("❌ User not found.")
        except Exception as e:
            await event.reply(f"❌ Error: {e}")

        # Delete the command message
        await event.delete()

# Rate limit for inviting members
INVITE_LIMIT = 50  # Number of invites per session
RATE_LIMIT_TIME = 60  # Time in seconds to wait before the next batch

# Command to invite all members from another group
for ubot in ubots:
    @ubot.on(events.NewMessage(pattern=fr'(?i)^{UBOT_HNDLR}inviteall (.*)'))
    async def invite_all_handler(event):
        user_id = event.sender_id

        # Check if the user is authorized
        if user_id != OWNER_ID and user_id not in SUDO_USERS:
            await event.reply("❌ You don't have permission to use this command.")
            logging.warning("Unauthorized access attempt by user_id: %s", user_id)
            return

        group_link = event.pattern_match.group(1)
        try:
            target_group = await event.client.get_entity(group_link)
            members = await event.client.get_participants(target_group)

            for idx, user in enumerate(members):
                try:
                    if user.id != (await event.client.get_me()).id:  # Don't invite yourself
                        await event.client(functions.channels.InviteToChannelRequest(
                            event.chat_id,
                            [user]
                        ))
                        logging.info(f"Invited {user.first_name} to the group.")
                        await asyncio.sleep(1)  # Delay between invites

                    # Check for limit and wait if necessary
                    if (idx + 1) % INVITE_LIMIT == 0:
                        await event.reply(f"✅ Invited {INVITE_LIMIT} members. Please wait for {RATE_LIMIT_TIME} seconds to continue.")
                        await asyncio.sleep(RATE_LIMIT_TIME)
                except Exception as e:
                    # Handle specific errors
                    if 'Privacy settings' in str(e):
                        await event.reply(f"❌ Cannot invite {user.first_name}: Privacy settings prevent this.")
                    elif 'Too many requests' in str(e):
                        await event.reply("❌ Rate limit reached. Please wait before trying again.")
                        break  # Stop inviting if rate limit is reached
                    else:
                        logging.warning(f"❌ Failed to invite {user.first_name}: {e}")

            await event.reply("✅ Finished inviting members.")
        except Exception as e:
            await event.reply(f"❌ Failed to invite members from {group_link}: {e}")

        # Delete the command message
        await event.delete()