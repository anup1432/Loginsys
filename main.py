import asyncio, sqlite3, datetime, os
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from aiogram import Bot, Dispatcher, types
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.functions.channels import GetFullChannelRequest

DB = "config.db"

# ---------- DATABASE ----------
def init_db():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS config (api_id TEXT, api_hash TEXT, session TEXT)")
    if not cur.execute("SELECT * FROM config").fetchone():
        cur.execute("INSERT INTO config VALUES ('','','')")
    con.commit(); con.close()

def get_config():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    row = cur.execute("SELECT * FROM config").fetchone()
    con.close()
    return row

def save_config(a,h,s):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("UPDATE config SET api_id=?, api_hash=?, session=?",(a,h,s))
    con.commit(); con.close()

# ---------- TELETHON ----------
client = None

async def load_client():
    global client
    api_id, api_hash, session = get_config()
    if not session: return
    client = TelegramClient(StringSession(session), int(api_id), api_hash)
    await client.start()

async def join_and_check(link):
    entity = await client.get_entity(link)
    await client.join_chat(entity)
    full = await client(GetFullChannelRequest(entity))
    age = (datetime.datetime.now(datetime.timezone.utc) - full.full_chat.date).days
    return entity.id, age

async def check_owner(chat_id):
    me = await client.get_me()
    perms = await client.get_permissions(chat_id, me)
    return perms.is_creator

# ---------- BOT ----------
bot = bot = Bot("8592232894:AAHuo1Y8dbsS4QNUqHvMqmbWzwrM3mskNqI")
dp = Dispatcher()

@dp.message()
async def handler(msg: types.Message):
    if not client:
        return await msg.reply("❌ Session not configured")

    if "t.me" not in msg.text:
        return await msg.reply("❌ Group link bhejo")

    chat_id, age = await join_and_check(msg.text)
    await msg.reply(f"✅ Joined\n📅 Group age: {age} days\n\n👉 Ab mere account ko OWNER banao")

    for _ in range(12):
        if await check_owner(chat_id):
            return await msg.reply("🎉 Ownership Verified")
        await asyncio.sleep(10)

    await msg.reply("❌ Ownership nahi di gayi")

# ---------- WEB ----------
app = FastAPI()
templates = Jinja2Templates("templates")

@app.get("/", response_class=HTMLResponse)
async def admin(req: Request):
    return templates.TemplateResponse("admin.html", {"request": req, "msg": ""})

@app.post("/", response_class=HTMLResponse)
async def save(req: Request, api_id: str = Form(...), api_hash: str = Form(...), session: str = Form(...)):
    save_config(api_id, api_hash, session)
    await load_client()
    return templates.TemplateResponse("admin.html", {"request": req, "msg": "Saved & Reloaded"})

# ---------- START ----------
async def start():
    init_db()
    await load_client()
    asyncio.create_task(dp.start_polling(bot))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT",8000)))

asyncio.run(start())
