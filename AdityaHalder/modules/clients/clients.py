import os
import sys
from pyrogram import Client
from motor.motor_asyncio import AsyncIOMotorClient
from pytgcalls import PyTgCalls

from ...console import (
    API_ID,
    API_HASH,
    STRING_SESSION,
    SESSION_STRING,
    BOT_TOKEN,
    MONGO_DB_URL,
    LOG_GROUP_ID,
    SUDOERS,
    LOGGER,
)

def async_config():
    LOGGER.info("Checking Variables ...")
    required_vars = {
        "API_ID": API_ID,
        "API_HASH": API_HASH,
        "BOT_TOKEN": BOT_TOKEN,
        "STRING_SESSION": STRING_SESSION,
        "MONGO_DB_URL": MONGO_DB_URL,
        "LOG_GROUP_ID": LOG_GROUP_ID,
    }

    for name, value in required_vars.items():
        if not value:
            LOGGER.error(f"'{name}' - Not Found!")
            sys.exit()

    LOGGER.info("All Required Variables Collected.")

def async_dirs():
    LOGGER.info("Initializing Directories ...")
    os.makedirs("downloads", exist_ok=True)
    os.makedirs("cache", exist_ok=True)

    # Clean old session files
    for file in os.listdir():
        if file.endswith((".session", ".session-journal")):
            os.remove(file)

    LOGGER.info("Directories Initialized.")

async_dirs()
async_config()

# Clients
app = Client("AdityaHalder", api_id=API_ID, api_hash=API_HASH, session_string=STRING_SESSION)
ass = Client("AdityaPlayer", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
bot = Client("AdityaServer", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Voice call client
call = PyTgCalls(app if not SESSION_STRING else ass)

def mongodbase():
    global mongodb
    try:
        LOGGER.info("Connecting To Your Database ...")
        client = AsyncIOMotorClient(MONGO_DB_URL)
        mongodb = client.AdityaHalder
        LOGGER.info("Connected To Your Database.")
    except Exception as e:
        LOGGER.error(f"MongoDB Connection Failed: {e}")
        sys.exit()

mongodbase()

async def sudo_users():
    sudoersdb = mongodb.sudoers
    data = await sudoersdb.find_one({"sudo": "sudo"})
    users = data["sudoers"] if data else []
    SUDOERS.extend([int(uid) for uid in users])
    LOGGER.info("Sudo Users Loaded.")

async def run_async_clients():
    LOGGER.info("Starting Userbot ...")
    await app.start()
    LOGGER.info("Userbot Started.")

    try:
        await app.send_message(LOG_GROUP_ID, "**Userbot Started.**")
    except:
        pass

    try:
        await app.join_chat("Neo_Supporter")
        await app.join_chat("The_Cute_boy_op")
    except:
        pass

    if SESSION_STRING:
        LOGGER.info("Starting Assistant ...")
        await ass.start()
        LOGGER.info("Assistant Started.")
        try:
            await ass.send_message(LOG_GROUP_ID, "**Assistant Started.**")
        except:
            pass
        try:
            await ass.join_chat("Neo_Supporter")
            await ass.join_chat("The_Cute_boy_op")
        except:
            pass

    LOGGER.info("Starting Helper Bot ...")
    await bot.start()
    LOGGER.info("Helper Bot Started.")
    try:
        await bot.send_message(LOG_GROUP_ID, "**Helper Bot Started.**")
    except:
        pass

    LOGGER.info("Starting PyTgCalls Client ...")
    await call.start()
    LOGGER.info("PyTgCalls Client Started.")

    await sudo_users()
