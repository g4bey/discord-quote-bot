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
            'hall_of_fame': None,
            'guild_id': guild_id,
            'langage': 'english',
            'channels': [],
            'scope': 'global'
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

def change_scope(guild_id, scope) -> None:
    guild_settings.update(
        {
            'scope': scope
        },
        Query().guild_id == guild_id
    )

def enable_channel(guild_id, channel_id) -> None:
    guild = select_guild(guild_id)
    channels = guild['channels']

    if channel_id not in channels:
        channels.append(channel_id)

        guild_settings.update(
            {
                'channels': channels
            },
            Query().guild_id == guild_id
        )

def disable_channel(guild_id, channel_id) -> None:
    guild = select_guild(guild_id)
    channels = guild['channels']

    if channel_id in channels:
        channels.remove(channel_id)

        guild_settings.update(
            {
                'channels': channels
            },
            Query().guild_id == guild_id
        )

def grab_channels(guild_id) -> None:
    guild = select_guild(guild_id)
    return guild.channels

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
