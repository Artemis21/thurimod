"""Set up the Discord client and command manager."""
import logging

import dslash
from nextcord import Embed

from .config import CONFIG
from .utils.checks import Context

log = logging.getLogger("thurimod")
bot = dslash.CommandClient(guild_id=CONFIG.discord.guild_id)


@bot.event
async def on_ready():
    """Log a message when the client is connected and the cache filled."""
    log.info(f"Logged in as {bot.user}.")


@bot.command()
async def about(ctx: Context):
    """Find out a bit more about the bot."""
    if not bot.user:
        # Not logged in yet (mainly done for type checking).
        return
    await ctx.response.send_message(embed=(
        Embed(
            title="About",
            description=(
                "Thuri Mod is a simple Discord moderation bot by "
                "[Artemis](https://arty.li) as a commission for Thurikyl#3380."
            ),
            colour=0xff2fd6,
        ).set_thumbnail(url=bot.user.display_avatar.url)
    ))


def mainloop():
    """Connect to Discord and run the bot mainloop."""
    bot.run(CONFIG.discord.token)
