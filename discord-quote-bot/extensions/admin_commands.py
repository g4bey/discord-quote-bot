from multiprocessing import context
import hikari
import lightbulb
from utils import guilds_settings, registerOrReset_guild, select_guild, change_global, get_config, change_hall_of_fame

plugin = lightbulb.Plugin("Admin-Commands")
plugin.add_checks(
    lightbulb.guild_only,
    lightbulb.has_guild_permissions(hikari.Permissions.ADMINISTRATOR)
)

conf = get_config()


# -----------------------------------------------------


@plugin.command
@lightbulb.command('hall_of_fame',
                   'If set, quotes will be sent in the hall of fame.')
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def hall_of_fame_grp(ctx: lightbulb.Context):
    pass


@hall_of_fame_grp.child
@lightbulb.command('set', 'Sets a channel as the hall of fame')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def toggle_scmd(ctx: lightbulb.Context):
    change_hall_of_fame(ctx.guild_id, ctx.channel_id)

    await ctx.respond('This channel has been set as the hall of fame.')


@hall_of_fame_grp.child
@lightbulb.command('unset', 'Unsets the hall of fame.')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def toggle_scmd(ctx: lightbulb.Context):
    change_hall_of_fame(ctx.guild_id, None)

    await ctx.respond('The hall of fame has been unset.')


# -----------------------------------------------------


@plugin.command
@lightbulb.command('global_mode', 'Enables and disables the global mode.')
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def global_mode_grp(ctx: lightbulb.context):
    pass


@global_mode_grp.child
@lightbulb.command('enable',
                   'The bot will reply in the channel it was invocated in.')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def enable_scmd(ctx: lightbulb.Context):
    change_global(ctx.guild_id, True)

    await ctx.respond('Global mode has been activated.')


@global_mode_grp.child
@lightbulb.command('disable',
                   'The bot will only reply in the hall of fame, if set.')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def disable_scmd(ctx: lightbulb.Context):
    change_global(ctx.guild_id, False)
    await ctx.respond('Global mode has been disabled.')


# -----------------------------------------------------

@plugin.command
@lightbulb.command('settings', 'Display the current settings')
@lightbulb.implements(lightbulb.SlashCommand)
async def display_settings(ctx: lightbulb.context):
    guild = select_guild(ctx.guild_id)

    if not guild:
        guild = registerOrReset_guild(ctx.guild_id)

    response = f"Guild Id: {guild['guild_id']}"

    response += "\nGlobal mode: "
    if guild['global']:
        response += "enable"
    else:
        response += "disabled"

    response += "\nHall of fame: "
    if guild['hall_of_fame']:
        response += f"<#{guild['hall_of_fame']}>"
        response += "\n"
    else:
        response += "unset"

    await ctx.respond(response)


@plugin.command
@lightbulb.command('reset', 'Reset setting for the bot.')
@lightbulb.implements(lightbulb.SlashCommand)
async def reset(ctx: lightbulb.context) -> None:
    registerOrReset_guild(ctx.guild_id)

    await ctx.respond('Settings have been reseted for this guild', reply=False)


# -----------------------------------------------------


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
