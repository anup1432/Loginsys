ownership.py

Telegram group/channel ownership verification module

from telethon.tl.functions.channels import GetParticipantRequest from telethon.tl.types import ChannelParticipantCreator

async def is_owner(client, chat): """ Check whether the logged-in Telethon account is OWNER of the group/channel :param client: Telethon client :param chat: group/channel entity or chat_id :return: True / False """ me = await client.get_me() try: participant = await client(GetParticipantRequest(chat, me.id)) return isinstance(participant.participant, ChannelParticipantCreator) except Exception: return False

async def wait_for_ownership(client, chat, timeout=120): """ Wait until ownership is given (polling) :param timeout: seconds :return: True if owner given within time """ import asyncio, time start = time.time()

while time.time() - start < timeout:
    if await is_owner(client, chat):
        return True
    await asyncio.sleep(10)

return False
