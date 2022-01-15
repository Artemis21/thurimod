"""Basic ban and kick commands."""
from typing import Optional

from nextcord import Member

from ...bot import bot
from ...utils.checks import Context


@bot.command()
async def kick(ctx: Context, member: Member, reason: Optional[str]):
    """Kick someone."""
    await member.kick()
    reason = f" for {reason}" if reason else ""
    await ctx.response.send_message(f"Kicked **{member}**{reason}!")


@bot.command()
async def ban(ctx: Context, member: Member, reason: Optional[str]):
    """Ban someone."""
    await member.ban()
    reason = f" for {reason}" if reason else ""
    await ctx.response.send_message(f"Banned **{member}**{reason}!")


@bot.command()
async def unban(ctx: Context, username: str):
    """Unban someone by username."""
    username = username.lower()
    to_unban, matches = None, []
    for ban in await ctx.guild.bans():
        if username == str(ban.user):
            to_unban = ban
            break
        if username.lower() in ban.user.name:
            matches.append(ban)
    if not to_unban:
        if len(matches) > 1:
            await ctx.response.send_message(f"Multiple matches for {username!r}.")
            return
        if not matches:
            await ctx.response.send_message(f"No matches for {username!r}.")
            return
        to_unban = matches[0]
    await ctx.guild.unban(to_unban.user)
    await ctx.response.send_message(f"Unbanned **{to_unban.user}**!")
