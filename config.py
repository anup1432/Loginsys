config.py

Runtime configuration loader (from database)

from database import get_config

class Config: api_id: int | None = None api_hash: str | None = None session: str | None = None

@classmethod
def load(cls):
    """Load config from database"""
    api_id, api_hash, session = get_config()

    cls.api_id = int(api_id) if api_id else None
    cls.api_hash = api_hash if api_hash else None
    cls.session = session if session else None

@classmethod
def is_ready(cls) -> bool:
    """Check if all required config values exist"""
    return bool(cls.api_id and cls.api_hash and cls.session)

@classmethod
def as_dict(cls):
    return {
        "api_id": cls.api_id,
        "api_hash": cls.api_hash,
        "session": cls.session,
    }
