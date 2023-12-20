import hikari
import lightbulb
from utils import get_config

conf = get_config()


plugin = lightbulb.Plugin("Bot-Administration")
guilds = [conf['owner_guild']]
plugin.add_checks(lightbulb.owner_only)

# -----------------------------------------------------


@plugin.command
@lightbulb.command("reload_extension", "reload extensions",
                   hidden=True, guilds=guilds)
@lightbulb.implements(lightbulb.SlashCommand)
async def reload_extension(ctx: lightbulb.Context):
    [ctx.bot.reload_extensions(ext) for ext in ctx.bot.extensions]
    await ctx.respond("Reloaded all extensions successfully. ;p", reply=False)


@plugin.command
@lightbulb.command("sync_application_commands",
                   "sync the accplication commands", hidden=True, guilds=guilds)
@lightbulb.implements(lightbulb.SlashCommand)
async def sync_application_commands(ctx: lightbulb.Context):
    await ctx.bot.sync_application_commands()
    await ctx.respond("Synced application commands", reply=False)


@plugin.command
@lightbulb.command("get_latency", "send the current latency",
                   hidden=True, guilds=guilds)
@lightbulb.implements(lightbulb.SlashCommand)
async def get_latency(ctx: lightbulb.Context):
    await ctx.respond(ctx.bot.heartbeat_latency, reply=False)


@plugin.command
@lightbulb.command("purge_commands", "purge the commands",
                   hidden=True, guilds=guilds)
@lightbulb.implements(lightbulb.SlashCommand)
async def purge_commands(ctx: lightbulb.Context):
    await ctx.bot.purge_application_commands(global_commands=True)
    await ctx.respond("Purged application commands", reply=False)


# -----------------------------------------------------


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)