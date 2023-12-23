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
@lightbulb.option(
    'option',
    'Set: This channel becomes the hall of fame.',
    choices=['set', 'unset'],
    required=True
)
@lightbulb.command('hall_of_fame',
                   'If set, quotes will be forward to this channel.', 
                   pass_options=True
                   )
@lightbulb.implements(lightbulb.SlashCommand)
async def hall_of_fame_toggle(ctx: lightbulb.SlashContext, option: str):
    if option == 'set':
        change_hall_of_fame(ctx.guild_id, ctx.channel_id)
        await ctx.respond('This channel has been set as the hall of fame')
    else:
        guild = select_guild(ctx.guild_id)
        if guild['hall_of_fame'] == ctx.get_channel().id:
            change_hall_of_fame(ctx.guild_id, None)
            await ctx.respond('This channel has been unset as the hall of fame.')
        else:
            await ctx.respond('This channel is not the hall of fame. Please check /settings')


# -----------------------------------------------------
    

@plugin.command
@lightbulb.option(
    'option',
    'Add or remove the channel from allowance list.',
    choices=['add', 'remove'],
    required=True
)
@lightbulb.command('channel',
                   'Allow the bot to send quotes in this channel. Only works with global & selective scope.', 
                   pass_options=True
                   )
@lightbulb.implements(lightbulb.SlashCommand)
async def channel_toggle(ctx: lightbulb.SlashContext, option: str):
    if option == 'add':
        enable_channel(ctx.guild_id, ctx.channel_id)
        await ctx.respond('This channel has been added to the list.')
    else:
        disable_channel(ctx.guild_id, ctx.channel_id)
        await ctx.respond('This channel has been removed from the list.')

# -----------------------------------------------------

@plugin.command
@lightbulb.option(
    'option',
    'Global: everywhere. Selective: only enabled channel. Laser: hall of fame only.',
    choices=['global', 'selective', 'laser'],
    required=True
)
@lightbulb.command('scope', 
                   'Pick the scope for the bot to send quotes in.', 
                   pass_options=True
                   )
@lightbulb.implements(lightbulb.SlashCommand)
async def scope(ctx: lightbulb.SlashContext, option: str):
    if option == 'global':
        change_scope(ctx.guild_id, 'global')
        await ctx.respond('Global scope has been activated.')
    elif option == 'selective':
        change_scope(ctx.guild_id, 'selective')
        await ctx.respond('Selective scope has been activated.')
    else:
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
