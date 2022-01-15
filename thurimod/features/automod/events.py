"""Register event handlers for the automod system."""
from nextcord import Message

from ...bot import bot
from ...config import CONFIG
from .filters import MESSAGE_FILTERS


@bot.listener
async def on_message(message: Message):
    """Delete a message if it does not pass our content filters."""
    if (not message.guild) or (message.guild.id != CONFIG.discord.guild_id):
        return
    if message.author.bot:
        return
    for filter in MESSAGE_FILTERS:
        if reason := filter(message):
            await message.delete()
            await message.channel.send(
                f"{message.author.mention}, your message was deleted because {reason}."
            )
            return
