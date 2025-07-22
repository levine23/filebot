from pyrogram import Client, filters
from database.database import add_user, del_user, full_userbase, present_user
from config import OWNER_ID
from pymongo import MongoClient
from pyrogram.errors import FloodWait
import asyncio


# Simpan user ke database (biar semua yang pernah interaksi tercatat)
@Client.on_message(filters.private)
async def save_user(client, message):
    await user_data.update_one(
        {"user_id": message.from_user.id},
        {"$set": {"user_id": message.from_user.id}},
        upsert=True
    )


# Broadcast hanya untuk OWNER
@Client.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast_message(client, message):
    if len(message.command) < 2:
        await message.reply("❌ Gunakan:\n`/broadcast pesan yang akan dikirim`")
        return

    text = message.text.split(None, 1)[1]
    sent = 0
    failed = 0

    users = await users_col.find().to_list(length=0)

    await message.reply(f"🚀 Mulai broadcast ke {len(users)} user...")

    for user in users:
        try:
            await client.send_message(user["user_id"], text)
            sent += 1
            await asyncio.sleep(0.1)
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception:
            failed += 1

    await message.reply(f"✅ Broadcast selesai!\nDikirim: {sent}\nGagal: {failed}")