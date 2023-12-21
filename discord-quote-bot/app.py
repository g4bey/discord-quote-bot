import aiohttp
import concurrent.futures
from utils import *
from os import name as os_name
import hikari
import asyncio
import lightbulb
from utils import get_config, registerOrReset_guild, remove_guild
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

bot = lightbulb.BotApp(
    token=token,
    intents=hikari.Intents.ALL,
    delete_unbound_commands=True,
    default_enabled_guilds=(conf['owner_guild'])
)

bot.load_extensions_from("./extensions/", must_exist=True)

@bot.listen()
async def on_guild_join(event: hikari.GuildJoinEvent) -> None:
    registerOrReset_guild(hikari.GuildJoinEvent)

@bot.listen()
async def on_guild_leave(event: hikari.GuildLeaveEvent) -> None:
    remove_guild(event.guild_id)

@bot.listen()
async def on_starting(event: hikari.StartingEvent) -> None:
    bot.d.loop = asyncio.get_running_loop()
    bot.d.aio_session = aiohttp.ClientSession()
    bot.d.process_pool = concurrent.futures.ProcessPoolExecutor()


if __name__ == "__main__":
    if os_name != "nt":
        import uvloop  #  ignore (uvloop does not exist on windows.)
        uvloop.install()
        
    bot.run(
        status=hikari.Status.ONLINE,
        activity=hikari.Activity(
            name="all of you, cuties!",
            type=hikari.ActivityType.LISTENING
        )
    )

    freeze_support()
