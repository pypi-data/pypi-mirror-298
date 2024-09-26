"""sopel-rainbow

A Sopel plugin to make things RAINBOW COLORED.
"""
from __future__ import annotations

import itertools
import random

from sopel import formatting, plugin
from sopel.config import types

# TODO: Consider making ud2 an install extra
# or just require it outright; in absolute terms, it isn't a heavy library
# (though relative to just this plugin, it's on the order of 100x the size)
try:
    import unicodedata2 as unicodedata
except ImportError:
    import unicodedata


class RainbowSection(types.StaticSection):
    order = types.ListAttribute(
        'order', default=[str(v) for v in (4, 7, 8, 3, 12, 2, 6)])
    """The order of color codes to use.

    Defaults to a standard ROYGBIV rainbow (assuming readers' clients use
    typical IRC color code mappings).
    """
    random_start = types.BooleanAttribute('random_start', default=False)
    """Whether to randomize the start color."""


def configure(config):
    config.define_section('rainbow', RainbowSection)
    config.rainbow.configure_setting(
        'order',
        'Specify the order of IRC color codes to use in the "rainbow":'
    )
    config.rainbow.configure_setting(
        'random_start',
        'Randomize start position in the rainbow?'
    )


def setup(bot):
    bot.config.define_section('rainbow', RainbowSection)


@plugin.commands('rainbow')
def rainbow_cmd(bot, trigger):
    """Make text into a rainbow."""
    text = formatting.plain(trigger.group(2) or '').strip()

    if not text:
        bot.reply("I can't make a rainbow out of nothing!")
        return plugin.NOLIMIT

    colors = bot.config.rainbow.order
    color_cycle = itertools.cycle(colors)

    if bot.config.rainbow.random_start:
        color_cycle = itertools.islice(
            # passing all of (iter, start, stop) is important;
            # passing only (iter, stop) will return a non-infinite iterator
            color_cycle, random.randrange(len(colors)), None,
        )

    bot.say(
        ''.join(
            char if unicodedata.category(char) == 'Zs'
            else formatting.color(char, next(color_cycle))
            for char in text
        )
    )
