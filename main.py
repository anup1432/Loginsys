import os
import asyncio
import sqlite3
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from bot import start_bot  # Aiogram bot logic

# ---------- DATABASE ----------
DB = "config.db"

def init_db():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS config (api_id TEXT, api_hash TEXT, session TEXT)")
    if not cur.execute("SELECT * FROM config").fetchone():
        cur.execute("INSERT INTO config VALUES ('','','')")
    con.commit()
    con.close()

def get_config():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    row = cur.execute("SELECT * FROM config").fetchone()
    con.close()
    return row

def save_config(a, h, s):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("UPDATE config SET api_id=?, api_hash=?, session=?", (a, h, s))
    con.commit()
    con.close()

# ---------- FASTAPI APP ----------
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def admin(req: Request):
    return templates.TemplateResponse("admin.html", {"request": req, "msg": ""})

@app.post("/", response_class=HTMLResponse)
async def save(req: Request, api_id: str = Form(...), api_hash: str = Form(...), session: str = Form(...)):
    save_config(api_id, api_hash, session)
    from userbot import load_client
    await load_client()
    return templates.TemplateResponse("admin.html", {"request": req, "msg": "Saved & Reloaded"})

# ---------- STARTUP ----------
@app.on_event("startup")
async def startup():
    # Initialize DB
    init_db()
    # Start Telethon client
    from userbot import load_client
    await load_client()
    # Start Aiogram bot in background
    asyncio.create_task(start_bot())
