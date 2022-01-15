"""Commands for the warning feature."""
from nextcord import Embed, Member
from sqlalchemy import select

from ...bot import bot
from ...database import make_session
from ...utils.checks import Context
from .models import Warning


@bot.command()
async def warn(ctx: Context, member: Member, reason: str):
    """Give someone a warning."""
    reason = reason.replace("\n", " ")
    async with make_session() as session:
        async with session.begin():
            session.add(Warning(user_id=member.id, reason=reason))
    await ctx.response.send_message(f"{member.mention} (**{member}**) has been warned: *{reason}*")


@bot.command()
async def warnings(ctx: Context, member: Member):
    """Check what warnings someone has."""
    async with make_session() as session:
        warnings = list(
            (await session.execute(select(Warning).where(Warning.user_id == member.id))).scalars()
        )
    if not warnings:
        await ctx.response.send_message(f"**{member}** has no warnings.")
    else:
        log = "\n".join(
            f"`{warning.id}` <t:{int(warning.created_at.timestamp())}>: {warning.reason}"
            for warning in warnings
        )
        await ctx.response.send_message(
            embed=(
                Embed(title=f"Warnings for {member}", description=log).set_footer(
                    text="Do '/delwarn (id)' to delete a warning."
                )
            )
        )


@bot.command()
async def delwarn(ctx: Context, id: int):
    """Delete a warning by ID."""
    async with make_session() as session:
        async with session.begin():
            warning = (
                (await session.execute(select(Warning).where(Warning.id == id))).scalars().first()
            )
            if warning:
                await session.delete(warning)
    if warning:
        await ctx.response.send_message(
            f"Deleted warning for <@{warning.user_id}>: *{warning.reason}*"
        )
    else:
        await ctx.response.send_message(f"No warning found by ID {id}.")
