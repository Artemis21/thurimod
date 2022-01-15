"""Command check wrappers."""
from nextcord import Guild, Interaction, Member, Permissions
from dslash import allow_roles

from ..config import CONFIG


class Context(Interaction):
    """Context passed to slash commands.

    This overwrites some type hints to apply specifically to commands used in a
    guild, since this bot's commands will only be registered in one guild.
    """

    guild: Guild
    user: Member


def has_permissions(ctx: Context, perms: Permissions) -> bool:
    """Check if a user has the given permissions."""
    if ctx.user.guild_permissions.administrator:
        return True
    return ctx.user.guild_permissions >= perms


admin_role = allow_roles(CONFIG.discord.admin_role_id, guild_id=CONFIG.discord.guild_id)
