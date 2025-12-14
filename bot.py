bot.py

Telegram bot logic (Aiogram)

import asyncio from aiogram import Bot, Dispatcher, types from aiogram.filters import CommandStart

from userbot import join_and_check, wait_until_owner

BOT_TOKEN = "8592232894:AAHuo1Y8dbsS4QNUqHvMqmbWzwrM3mskNqI"

bot = Bot(BOT_TOKEN) dp = Dispatcher()

@dp.message(CommandStart()) async def start_cmd(message: types.Message): await message.reply( "👋 Welcome!\n\n" "👉 Mujhe group / channel ka link bhejo.\n" "Main join karke group age check karunga aur ownership verify karunga." )

@dp.message() async def handle_link(message: types.Message): text = message.text or ""

if "t.me" not in text:
    return await message.reply("❌ Valid Telegram group link bhejo")

try:
    entity, age_days = await join_and_check(text)
except Exception as e:
    return await message.reply(f"❌ Join error: {e}")

await message.reply(
    f"✅ Group joined successfully\n"
    f"📅 Group age: {age_days} days\n\n"
    f"👉 Ab mere account ko OWNER banao (2 minute ke andar)"
)

# wait for ownership
verified = await wait_until_owner(entity, timeout=120)

if verified:
    await message.reply("🎉 Ownership verified successfully!")
else:
    await message.reply("❌ Ownership time me nahi di gayi")

async def start_bot(): """Start bot polling""" await dp.start_polling(bot)
