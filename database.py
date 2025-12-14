database.py

SQLite database for saving admin panel configuration

import sqlite3

DB_NAME = "config.db"

def init_db(): """Initialize database and config table""" conn = sqlite3.connect(DB_NAME) cur = conn.cursor() cur.execute( """ CREATE TABLE IF NOT EXISTS config ( id INTEGER PRIMARY KEY, api_id TEXT, api_hash TEXT, session TEXT ) """ )

# insert default row if empty
cur.execute("SELECT COUNT(*) FROM config")
if cur.fetchone()[0] == 0:
    cur.execute(
        "INSERT INTO config (api_id, api_hash, session) VALUES (?, ?, ?)",
        ("", "", "")
    )

conn.commit()
conn.close()

def get_config(): """Return (api_id, api_hash, session)""" conn = sqlite3.connect(DB_NAME) cur = conn.cursor() cur.execute("SELECT api_id, api_hash, session FROM config WHERE id=1") row = cur.fetchone() conn.close() return row

def save_config(api_id: str, api_hash: str, session: str): """Update config values""" conn = sqlite3.connect(DB_NAME) cur = conn.cursor() cur.execute( "UPDATE config SET api_id=?, api_hash=?, session=? WHERE id=1", (api_id, api_hash, session) ) conn.commit() conn.close()
