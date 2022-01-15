"""Commands for the muting system."""
from typing import Optional

from nextcord import Forbidden, Member, PermissionOverwrite, Role
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...bot import bot
from ...database import make_session
from ...utils.checks import Context
from .models import MuteSettings

MUTE_ROLE_PERMS = PermissionOverwrite(send_messages=False, connect=False)


async def get_settings(ctx: Context, session: AsyncSession) -> Optional[MuteSettings]:
    """Get the mute settings for a server, if any."""
    return (
        (await session.execute(select(MuteSettings).where(MuteSettings.guild_id == ctx.guild.id)))
        .scalars()
        .first()
    )


async def create_role(ctx: Context, session: AsyncSession) -> Role:
    """Create a mute role when a server doesn't have one."""
    role = await ctx.guild.create_role(name="Muted")
    for channel in ctx.guild.channels:
        try:
            await channel.edit(
                overwrites={**channel.overwrites, role: MUTE_ROLE_PERMS}
            )  # type: ignore
        except Forbidden:
            continue
    if settings := await get_settings(ctx, session):
        settings.mute_role = role.id  # type: ignore
    else:
        session.add(MuteSettings(guild_id=ctx.guild.id, mute_role=role.id))  # type: ignore
    return role


async def get_role(ctx: Context, session: AsyncSession) -> Optional[Role]:
    """Get the mute role for the server, if it has one."""
    settings = await get_settings(ctx, session)
    if (not settings) or (not settings.mute_role):
        return None
    return ctx.guild.get_role(settings.mute_role)


@bot.command()
async def mute(ctx: Context, user: Member, reason: Optional[str]):
    """Mute someone."""
    await ctx.response.defer()
    async with make_session() as session:
        async with session.begin():
            role = await get_role(ctx, session)
            if not role:
                role = await create_role(ctx, session)
    await user.add_roles(role)
    reason = f" for {reason}" if reason else ""
    await ctx.followup.send(f"Muted **{user}**{reason}!")


@bot.command()
async def unmute(ctx: Context, user: Member):
    """Unmute someone."""
    async with make_session() as session:
        mute_role = await get_role(ctx, session)
    if mute_role in user.roles:
        await user.remove_roles(mute_role)
        await ctx.response.send_message(f"Unmuted **{user}**.")
    else:
        await ctx.response.send_message(f"**{user}** is not muted.")
