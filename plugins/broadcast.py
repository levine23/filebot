from pyrogram import Client, filters
from config import OWNER_ID
from database import user_data
from pyrogram.errors import FloodWait
import asyncio

# Simpan user saat DM (pakai fungsi dari database.py)
@Client.on_message(filters.private)
async def save_user(client, message):
    if not await user_data.find_one({'_id': message.from_user.id}):
        await user_data.insert_one({'_id': message.from_user.id})


# Broadcast command khusus OWNER
@Client.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast(client, message):
    if len(message.command) < 2:
        await message.reply("❌ Gunakan:\n`/broadcast pesan`")
        return

    text = message.text.split(None, 1)[1]
    sent = 0
    failed = 0

    users = user_data.find()

    await message.reply(f"🚀 Broadcast mulai...")

    async for user in users:
        try:
            await client.send_message(user['_id'], text)
            sent += 1
            await asyncio.sleep(0.1)
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception:
            failed += 1

    await message.reply(f"✅ Broadcast selesai!\nDikirim: {sent}\nGagal: {failed}")