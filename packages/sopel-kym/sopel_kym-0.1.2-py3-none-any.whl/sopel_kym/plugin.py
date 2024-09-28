"""sopel-kym

Meme definition plugin for Sopel IRC bots.
"""
from __future__ import annotations

import memedict

from sopel import plugin


PLUGIN_PREFIX = '[kym] '


@plugin.command('kym')
@plugin.output_prefix(PLUGIN_PREFIX)
def search(bot, trigger):
    query = trigger.group(2)

    if not query:
        bot.reply("What meme am I supposed to look up?")
        return plugin.NOLIMIT

    result = define_meme(query)

    if result is None:
        bot.reply("No results.")
        return

    _, url = memedict.search_meme(query)

    # Sometimes the `url` will be None for some reason
    # It's better to just output the `result` if it exists anyway, without
    # linking back to the site, than to throw an error.
    bot.say(result, truncation=' […]', trailing=(' | ' + url) if url else '')


@plugin.url(r'https?://knowyourmeme\.com/memes/([^/?#]+)')
@plugin.output_prefix(PLUGIN_PREFIX)
def link(bot, trigger):
    query = trigger.group(1)

    if not query:
        return plugin.NOLIMIT

    result = define_meme(query.replace('-', ' '))

    if result is None:
        return plugin.NOLIMIT

    bot.say(result, truncation=' […]')


def define_meme(name):
    result = memedict.search(name)

    if not result:
        return None

    return result
