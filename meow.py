from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, BotCommand, CopyTextButton
import asyncio
import json
import os
import secrets
import random

bot = Bot("token")
dp = Dispatcher()
DB_FILE = "files.json"

cat_facts = [
    "cats spend thirty pewcent of theiw day gwooming themselves",
    "a cat's puww can vibwate at fwequencies fwom 25 to 150 hewtz",
    "cats have ovew twenty vocalizations, including the standawd meow",
    "a gwoup of cats is cawwed a clowdew ow glawing",
    "cats can wotate theiw eaws 180 degwees",
    "the oldest known pet cat existed 9,500 yeaws ago",
    "cats spend seventy pewcent of theiw lives sweeping",
    "a cat's nose pwint is unique, wike a human fingew-pwint",
    "cats can jump up to six times theiw wength",
    "the wichest cat in the wowld had seven miwwion dowwaws"
]

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

files = load_db()

@dp.message(Command("start"))
async def start(m: Message):
    args = m.text.split()
    if len(args) == 1:
        await m.answer("meoww")
    else:
        fid = args[1]
        if fid in files:
            await m.answer("meowsege:")
            await bot.copy_message(m.chat.id, m.chat.id, files[fid]["message_id"])

@dp.message(Command("meow"))
async def meow_cmd(m: Message):
    if m.reply_to_message:
        fid = secrets.token_urlsafe(16)
        files[fid] = {
            "message_id": m.reply_to_message.message_id
        }
        save_db(files)
        link = f"t.me/{(await bot.me()).username}?start={fid}"
        fact = random.choice(cat_facts)
        kb = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="copy wink", copy_text=CopyTextButton(text=link))
        ]])
        await m.answer(fact, reply_markup=kb)
    else:
        await m.answer("wepwy to a meowsege to genewate a shawe wink!")
 
@dp.message()
async def save(m: Message):
    pass

async def set_commands():
    await bot.set_my_commands([
        BotCommand(command="start", description="stawt the bot, meoww!"),
        BotCommand(command="meow", description="genewate shawe wink with cat fact")
    ])

async def main():
    await set_commands()
    await dp.start_polling(bot)

asyncio.run(main())