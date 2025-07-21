from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pymongo import MongoClient
from config import MONGO_URL, OWNER_ID  # ✅ ambil dari config

mongo = MongoClient(MONGO_URL)
db = mongo["filebot"]
buttons_col = db["buttons"]

@Client.on_message(filters.command("addbutton") & filters.user(OWNER_ID))
async def add_button(_, message):
    try:
        _, data = message.text.split(" ", 1)
        text, url = data.split("|", 1)
        await buttons_col.insert_one({"text": text.strip(), "url": url.strip()})
        await message.reply(f"✅ Button ditambahkan: `{text.strip()}` | `{url.strip()}`")
    except Exception:
        await message.reply("❌ Format salah!\nGunakan:\n`/addbutton Teks | URL`")


@Client.on_message(filters.command("listbutton") & filters.user(OWNER_ID))
async def list_button(_, message):
    buttons = await buttons_col.find().to_list(length=100)
    if not buttons:
        await message.reply("📭 Tidak ada button.")
        return
    text = "**Daftar Button:**\n"
    for i, btn in enumerate(buttons, 1):
        text += f"{i}. `{btn['text']}` | `{btn['url']}`\n"
    await message.reply(text)


@Client.on_message(filters.command("delbutton") & filters.user(OWNER_ID))
async def del_button(_, message):
    try:
        _, idx = message.text.split(" ", 1)
        idx = int(idx) - 1
        buttons = await buttons_col.find().to_list(length=100)
        if idx < 0 or idx >= len(buttons):
            raise Exception
        deleted = buttons[idx]
        await buttons_col.delete_one({"_id": deleted["_id"]})
        await message.reply(f"🗑️ Button dihapus: `{deleted['text']}` | `{deleted['url']}`")
    except Exception:
        await message.reply("❌ Format salah atau index tidak ada.\nGunakan:\n`/delbutton <nomor>`")


@Client.on_message(filters.command("buttons"))
async def show_buttons(_, message):
    buttons = await buttons_col.find().to_list(length=100)
    if not buttons:
        await message.reply("📭 Tidak ada button.")
        return
    markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton(btn["text"], url=btn["url"])] for btn in buttons]
    )
    await message.reply("🔘 Berikut button yang tersedia:", reply_markup=markup)