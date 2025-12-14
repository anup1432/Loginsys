age.py

Telegram group/channel age calculation

import datetime from telethon.tl.functions.channels import GetFullChannelRequest

async def get_group_age_days(client, entity): """ Return group/channel age in days :param client: Telethon client :param entity: group/channel entity :return: int | None """ full = await client(GetFullChannelRequest(entity)) created = full.full_chat.date

if not created:
    return None

now = datetime.datetime.now(datetime.timezone.utc)
return (now - created).days

async def get_group_age_text(client, entity): """ Return human readable age text Example: '2 years 3 months 5 days' """ full = await client(GetFullChannelRequest(entity)) created = full.full_chat.date

if not created:
    return "Unknown"

delta = datetime.datetime.now(datetime.timezone.utc) - created
days = delta.days

years = days // 365
days %= 365
months = days // 30
days %= 30

parts = []
if years:
    parts.append(f"{years} year{'s' if years > 1 else ''}")
if months:
    parts.append(f"{months} month{'s' if months > 1 else ''}")
if days:
    parts.append(f"{days} day{'s' if days > 1 else ''}")

return " ".join(parts) if parts else "0 days"
