userbot.py

Telethon user account logic: join group, check age, verify ownership

from telethon import TelegramClient from telethon.sessions import StringSession from telethon.errors import UserAlreadyParticipantError from telethon.tl.functions.messages import ImportChatInviteRequest

from config import Config from age import get_group_age_days from ownership import is_owner, wait_for_ownership

client: TelegramClient | None = None

async def start_userbot(): """Initialize and start Telethon client using runtime config""" global client Config.load()

if not Config.is_ready():
    raise RuntimeError("Config not ready: API_ID / API_HASH / SESSION missing")

client = TelegramClient(
    StringSession(Config.session),
    Config.api_id,
    Config.api_hash,
)

await client.start()
return client

async def ensure_started(): """Ensure userbot client is running""" global client if client is None or not client.is_connected(): await start_userbot()

async def join_group(link: str): """Join group/channel using invite link or public link""" await ensure_started()

try:
    if "/+" in link or "joinchat" in link:
        hash_part = link.split("/")[-1]
        return await client(ImportChatInviteRequest(hash_part))
    else:
        entity = await client.get_entity(link)
        try:
            await client.join_chat(entity)
        except UserAlreadyParticipantError:
            pass
        return entity
except Exception as e:
    raise RuntimeError(f"Join failed: {e}")

async def join_and_check(link: str): """ Join group and return (chat_entity, age_days) """ entity = await join_group(link) age_days = await get_group_age_days(client, entity) return entity, age_days

async def check_ownership(entity): """Check if userbot is owner""" await ensure_started() return await is_owner(client, entity)

async def wait_until_owner(entity, timeout: int = 120): """Wait until ownership is granted (polling)""" await ensure_started() return await wait_for_ownership(client, entity, timeout=timeout)
