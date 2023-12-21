from tinydb import TinyDB, Query
from tinydb.table import Document

from utils import get_config
from tinydb_smartcache import SmartCacheTable

# -----------------------------------------------------


db_name = get_config().get('db_name') or 'database.db'

db = TinyDB(db_name)
db.table_class = SmartCacheTable

guild_settings = db.table('guild_settings')

def registerOrReset_guild(guild_id) -> Document:
    guild_settings.upsert(
        {
            'global': True,
            'hall_of_fame': None,
            'guild_id': guild_id
        },
        Query().guild_id == guild_id
    )

    return select_guild(guild_id)

def change_global(guild_id, value) -> None:
    guild_settings.update(
        {
            'global': value
        },
        Query().guild_id == guild_id
    )

def change_hall_of_fame(guild_id, channel_id) -> None:
    guild_settings.update(
        {
            'hall_of_fame': channel_id
        },
        Query().guild_id == guild_id
    )

def remove_guild(guild_id) -> None:
    guild_settings.remove(Query().guild_id == guild_id)

def select_guild(guild_id) -> Document | None:
    return guild_settings.get(Query().guild_id == guild_id)
