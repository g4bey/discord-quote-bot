from secrets import token_hex
import hikari
import lightbulb
from tinydb import Query
from utils import build_image, select_guild
from io import BytesIO
import datetime
from .errors_handling import CharacterLimitException
from .errors_handling import NoChannelAttributed
from .errors_handling import MissingParameterException
import typing

plugin = lightbulb.Plugin("Quote-Maker")
plugin.add_checks(lightbulb.guild_only)


# -----------------------------------------------------

def veriy_field(quote: str, username: str) -> None:
    """Make sure the field have appropriate lengh"""

    if not quote:
        raise MissingParameterException('quote')

    if len(quote) > 1000:
        raise CharacterLimitException(1000, 'quote')

    if len(username) > 38:
        raise CharacterLimitException(38, 'username')

async def handle_image(
    ctx: lightbulb.Context,
    username: typing.Union[hikari.Member, str],
    quote: str,
    pfp=None,
    custom_txt=None
) -> None:
    
    if not pfp:
        # pfp = ctx.bot.application.icon_url  
        pfp = hikari.File("./assets/default.jpg")

    attachment = {}
    avatar = BytesIO()
    async with pfp.stream() as stream:
        async for chunk in stream:
            avatar.write(chunk)

    loop = ctx.bot.d.loop

    image = await loop.run_in_executor(ctx.bot.d.process_pool, build_image, username, quote, avatar, custom_txt)
    attachment['attachment'] = image

    await process_response(ctx, attachment)

async def handle_embed(
    ctx: lightbulb.Context,
    username: typing.Union[hikari.Member, str],
    quote: str,
    pfp=None,
    custom_txt=None
) -> None:

    if not pfp:
        # pfp = ctx.bot.application.icon_url  
        pfp = hikari.File("./assets/default.jpg")

    attachment = {}

    embed = hikari.Embed(
    title=f'{username}:',
    description=quote,
    color=hikari.Color.from_hex_code(f"#{token_hex(3)}")
    )    

    embed.set_author(name=f'Quoted by {ctx.author.username}')
    embed.set_thumbnail(pfp)
        
    if custom_txt:
        embed.set_footer(custom_txt)

    attachment['embed'] = embed

    await process_response(ctx, attachment)

async def process_response(
    ctx: lightbulb.Context, attachment
) -> None:
    
    guild = select_guild(ctx.guild_id)
    current_channel = ctx.get_channel().id

    hall_of_fame = guild.get('hall_of_fame')
    scope = guild.get('scope')
    channels = guild.get('channels')

    if hall_of_fame:
        await ctx.bot.rest.create_message(
            hall_of_fame,
            f'A new quote was submitted by {ctx.author.mention}',
            **attachment
        )

        if hall_of_fame != current_channel:
            if scope == 'global' or scope == 'selective' and current_channel in channels: 
                await ctx.respond('Here is your quote!', **attachment)
            # else it has to be selective.

            # sending it to the hall of fame.
            channel = ctx.get_guild().get_channel(hall_of_fame).mention
            await ctx.respond(f'You quote was sent straight to {channel}', reply=False)
        else:
            await ctx.respond("Here we go!", delete_after=0)
    elif scope == 'global' or scope == 'selective' and current_channel in channels:
        await ctx.respond('Here is your quote!', **attachment)

# -----------------------------------------------------

@plugin.command
@lightbulb.add_cooldown(15.0, 1, lightbulb.UserBucket)
@lightbulb.command(
    "quote_this",
    "Click to quote this message.",
    auto_defer=True
)
@lightbulb.implements(lightbulb.MessageCommand)
async def quote_this_cmd(
    ctx: lightbulb.MessageContext
) -> None:
    target = ctx.options.target
    avatar = target.author.avatar_url
    username = f"{target.author.username}"
    quote = target.content
    date = target.created_at

    veriy_field(quote, username)

    await handle_image(ctx, username, quote, avatar, date)


@plugin.command
@lightbulb.add_cooldown(15.0, 1, lightbulb.UserBucket)
@lightbulb.command(
    "embed_this",
    "Click to embed this message.",
    auto_defer=True
)
@lightbulb.implements(lightbulb.MessageCommand)
async def embed_this_cmd(
    ctx: lightbulb.MessageContext
) -> None:

    target = ctx.options.target
    avatar = target.author.avatar_url
    username = f"{target.author.username}"
    quote = target.content
    date = target.created_at

    veriy_field(quote, username)
    
    await handle_embed(ctx, username, quote, avatar, date)


"""
@lightbulb.option(
    'type',
    'The bot can either generate an image, or send an embed.',
    choices=['image', 'embed']
)
"""

@plugin.command
@lightbulb.command(
    'embeded', 
    'Remember these few words forever!', 
    inherit_checks=True,
    pass_options=True,
    auto_defer=True
)
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def embeded(ctx: lightbulb.SlashContext):
    pass

@embeded.child
@lightbulb.add_cooldown(15.0, 1, lightbulb.UserBucket)
@lightbulb.option(
    'custom_txt',
    'Whatever you want to write!',
    required=False,
    default = str()
)
@lightbulb.option(
    'content',
    'The text you would like to quote',
    required=True
)
@lightbulb.option(
    'user',
    'The author of the quote',
    hikari.Member,
    default=lightbulb.SlashContext.author,
    required=True
)
@lightbulb.command(
    'quote', 'Make it an embed.',
    inherit_checks=True,
    pass_options=True,
    auto_defer=True
)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def quote_embed(
    ctx: lightbulb.SlashContext,  
    user: hikari.Member,
    content: str, 
    custom_txt: str = str()
    ):

    avatar = user.avatar_url
    await handle_embed(ctx, user, content, avatar, custom_txt)

@embeded.child
@lightbulb.add_cooldown(15.0, 1, lightbulb.UserBucket)
@lightbulb.option(
    'custom_txt',
    'Whatever you want to write!',
    required=False,
    default = str()
)
@lightbulb.option(
    'content',
    'The text you would like to quote',
    required=True
)
@lightbulb.command(
    'quote_me', 'Make it an image.',
    inherit_checks=True,
    pass_options=True,
    auto_defer=True
)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def quote_me_embed(    
    ctx: lightbulb.SlashContext,  
    content: str, 
    custom_txt: str = str()
    ):

    username = f"{ctx.username}"
    avatar = ctx.user.avatar_url

    veriy_field(content, username)
    await handle_image(ctx, username, content, avatar, custom_txt)



@plugin.command
@lightbulb.command(
    'picture', 
    'Remember these few words forever!', 
    inherit_checks=True,
    pass_options=True,
    auto_defer=True
)
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def pictured(ctx: lightbulb.SlashContext):
    pass

@pictured.child
@lightbulb.add_cooldown(15.0, 1, lightbulb.UserBucket)
@lightbulb.option(
    'custom_txt',
    'Whatever you want to write!',
    required=False,
    default = str()
)
@lightbulb.option(
    'content',
    'The text you would like to quote',
    required=True
)
@lightbulb.option(
    'user',
    'The author of the quote',
    hikari.Member,
    default=lightbulb.SlashContext.author,
    required=True
)
@lightbulb.command(
    'quote', 'Make it an image.',
    inherit_checks=True,
    pass_options=True,
    auto_defer=True
)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def quote_image(    
    ctx: lightbulb.SlashContext,  
    user: hikari.Member,
    content: str, 
    custom_txt: str = str()
    ):

    username = f"{user.username}"
    avatar = user.avatar_url

    veriy_field(content, username)
    await handle_image(ctx, username, content, avatar, custom_txt)

@pictured.child
@lightbulb.add_cooldown(15.0, 1, lightbulb.UserBucket)
@lightbulb.option(
    'custom_txt',
    'Whatever you want to write!',
    required=False,
    default = str()
)
@lightbulb.option(
    'content',
    'The text you would like to quote',
    required=True
)
@lightbulb.command(
    'quote_me', 'Make it an image.',
    inherit_checks=True,
    pass_options=True,
    auto_defer=True
)
@lightbulb.implements(lightbulb.SlashSubCommand)
async def quote_me_image(    
    ctx: lightbulb.SlashContext,  
    content: str, 
    custom_txt: str = str()
    ):

    username = f"{ctx.username}"
    avatar = ctx.user.avatar_url

    veriy_field(content, username)
    await handle_image(ctx, username, content, avatar, custom_txt)

# -----------------------------------------------------


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp) -> None:
    bot.remove_plugin(plugin)
