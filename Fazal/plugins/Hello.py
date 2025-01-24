import logging
from telethon import events
from Fazal import ubots, OWNER_ID, SUDO_USERS  # Ensure these are defined
from telethon.errors import UserBannedInChannelError

# Logging configuration
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)

for ubot in ubots:
    @ubot.on(events.NewMessage(pattern=r'(?i)^(hello|hi)$'))
    async def hello_handler(event):
        user_id = event.sender_id

        # Check if the user is authorized
        if user_id != OWNER_ID and user_id not in SUDO_USERS:
            logging.warning("Unauthorized access attempt by user_id: %s", user_id)
            return

        try:
            if event.is_reply:
                replied_user = await event.get_reply_message()
                if replied_user:
                    await replied_user.reply("👋 Hello")
                    logging.info(f"Replied to {replied_user.sender.first_name} with a greeting.")
                else:
                    logging.warning("Reply message not found.")
            else:
                await event.reply("🔰 Hi")
                logging.info("Sent a greeting to the user directly.")

            # Delete the command message
            await event.delete()

        except UserBannedInChannelError:
            logging.error("Bot is banned from sending messages in this channel.")
        except Exception as e:
            logging.error("Error in hello handler: %s", e)