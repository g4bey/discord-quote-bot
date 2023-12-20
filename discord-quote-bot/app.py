import aiohttp
import concurrent.futures
from utils import *
import logging
from os import listdir, getenv, name as os_name
import hikari
import asyncio
import lightbulb
from utils import get_config
from utils import guilds_settings
from tinydb import Query
from multiprocessing import freeze_support


# LOADING THE CONFIGURATION FILE
# -----------------------------------------------------
conf = get_config()

logger = conf['logger']
token = conf['token']


# SETTING UP LOGGING
# -----------------------------------------------------
init_logger(logger)

# SETTING UP THE DISCORD BOT
# -----------------------------------------------------
# default_enabled_guilds = ()


bot = lightbulb.BotApp(
    token=token,
    intents=hikari.Intents.ALL,
    delete_unbound_commands=True,
    default_enabled_guilds=(conf['owner_guild'])
)

bot.load_extensions_from("./extensions/", must_exist=True)

@bot.listen()
async def on_guild_join(event: hikari.GuildJoinEvent) -> None:
    guilds_settings.upsert(
        {
            'guild_id': event.guild_id,
            'global': True,
            'hall_of_fame': None
        },
        Query().guild_id == event.guild_id
    )

@bot.listen()
async def on_guild_leave(event: hikari.GuildLeaveEvent) -> None:
    guilds_settings.remove(Query().guild_id == event.guild_id)

@bot.listen()
async def on_starting(event: hikari.StartingEvent) -> None:
    bot.d.loop = asyncio.get_running_loop()
    bot.d.aio_session = aiohttp.ClientSession()
    bot.d.process_pool = concurrent.futures.ProcessPoolExecutor()



if __name__ == "__main__":
    if os_name != "nt":
        import uvloop  # type: ignore (uvloop does not exist on windows.)
        uvloop.install()
        
    bot.run(
        status=hikari.Status.ONLINE,
        activity=hikari.Activity(
            name="all of you, cuties!",
            type=hikari.ActivityType.LISTENING
        )
    )

    freeze_support()
