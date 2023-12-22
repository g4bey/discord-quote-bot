from time import strftime
from utils import get_config
from utils import create_if_missing
from PIL import Image, ImageOps, ImageDraw, ImageFont
from math import floor
from textwrap import fill
from datetime import datetime
from io import BytesIO
from hikari import Bytes
from secrets import token_hex


# -----------------------------------------------------


conf = get_config()

# -----------------------------------------------------


WHITE_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (43, 42, 40)
QUOTE_IMG_SIZE = (1120, 400)
MODE = 'RGBA'
BORDER_WIDTH = (5, 5, 5, 5)
PADDING = 20

# -----------------------------------------------------


def build_image(username, quote, profile_picture, date_txt):
    """Build the quote and return it as a hikari.Bytes object"""

    # Creating the base for the quote
    pfp = Image.open(profile_picture)
    base = Image.new(mode=MODE, size=QUOTE_IMG_SIZE, color=BACKGROUND_COLOR)
    pfp.convert(MODE)
    pfp = pfp.resize((base.height, base.height))
    base.paste(pfp, (0, 0))
    base = ImageOps.expand(base, border=BORDER_WIDTH, fill=WHITE_COLOR)
    textLayer = ImageDraw.Draw(base)

    # Adding the quote text.
    unformated_quote = "« " + ' '.join(quote.split('\n')) + " »"
    lengh_unformated_quote = len(unformated_quote)
    if lengh_unformated_quote < 111:
        quote_chara_width = 50
    elif lengh_unformated_quote < 222:
        quote_chara_width = 40
    elif lengh_unformated_quote < 333:
        quote_chara_width = 30
    else:
        quote_chara_width = 25
    quote_fnt = ImageFont.truetype(
        "assets/fonts/roboto_flex_variable.ttf", quote_chara_width
    )
    text_box_width = base.width - (pfp.width + PADDING + BORDER_WIDTH[2] + 5)
    quote_lengh = textLayer.textlength(unformated_quote, font=quote_fnt)
    avarage_chara_width = quote_lengh / len(unformated_quote)
    max_chara_per_line = floor(text_box_width / avarage_chara_width)
    wrapped_text = fill(
        unformated_quote,
        width=max_chara_per_line,
        break_long_words=True,
        fix_sentence_endings=True
    )
    textLayer.multiline_text(
        (pfp.width + PADDING,
         PADDING),
        wrapped_text,
        font=quote_fnt,
        fill=WHITE_COLOR,
        align='center'
    )

    # Adding the attributions
    credits_fnt = ImageFont.truetype(
        "assets/fonts/roboto_mono_bold_variable.ttf", 25
    )

    credits_txt = f'{username}\n{date_txt}'
    longest = username if len(username) >= 10 else date_txt
    offset = textLayer.textlength(
        longest,
        font=credits_fnt
    )
    textLayer.text(
        (
            base.width - (offset + 15),
            base.height - 75
        ),
        credits_txt,
        font=credits_fnt,
        fill=WHITE_COLOR,
        align='right'
    )

    result_byte = BytesIO()
    base.save(result_byte, "png")
    result_byte.seek(0)

    return Bytes(result_byte, f"{token_hex(10)}.png")
