from multiprocessing import context
import hikari
import lightbulb
from utils import *
from dateutil.parser import parse

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
@lightbulb.command('channel',
                   'Allow to generate the quote in this channel')
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def hall_of_fame_grp(ctx: lightbulb.Context):
    pass

@hall_of_fame_grp.child
@lightbulb.command('add', 'Adds the channel to the list.')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def toggle_scmd(ctx: lightbulb.Context):
    enable_channel(ctx.guild_id, ctx.channel_id)

    await ctx.respond('This channel has been added to the list.')

@hall_of_fame_grp.child
@lightbulb.command('remove', 'Remove the channel from the list.')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def toggle_scmd(ctx: lightbulb.Context):
    disable_channel(ctx.guild_id, ctx.channel_id)

    await ctx.respond('This channel has been removed from the list.')


# -----------------------------------------------------

@plugin.command
@lightbulb.command('scope', 'Pick the scope for the bot operate in.')
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def scope_grp(ctx: lightbulb.context):
    pass

@scope_grp.child
@lightbulb.command('global',
                   'The bot will post from anywhere.')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def global_scope(ctx: lightbulb.Context):
    change_scope(ctx.guild_id, 'global')
    await ctx.respond('Global scope has been activated.')

@scope_grp.child
@lightbulb.command('selective',
                   'The bot will only post where it\'s been manually allowed.')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def selective_scope(ctx: lightbulb.Context):
    change_scope(ctx.guild_id, 'selective')
    await ctx.respond('Selective scope has been activated.')

@scope_grp.child
@lightbulb.command('laser',
                   'Only the hall of fame will see images from the bot.')
@lightbulb.implements(lightbulb.SlashSubCommand)
async def laser_scope(ctx: lightbulb.Context):
    change_scope(ctx.guild_id, 'ultraSelective')
    await ctx.respond('Laser scope has been activated.')



# -----------------------------------------------------

@plugin.command
@lightbulb.command('settings', 'Display the current settings')
@lightbulb.implements(lightbulb.SlashCommand)
async def display_settings(ctx: lightbulb.context):
    guild = select_guild(ctx.guild_id)

    if not guild:
        guild = registerOrReset_guild(ctx.guild_id)

    response = f"Guild Id: {guild['guild_id']}"

    scope = guild['scope']
    response += f"\nScope: {scope}"
    if scope == 'selective':
        channels = guild['channels']
        response += f", channels = {channels}"

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
