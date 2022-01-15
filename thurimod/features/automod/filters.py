"""The different automod content filters we apply."""
import re
from typing import Optional

from nextcord import Message


def invite_link(message: Message) -> Optional[str]:
    """Check if a message contains an invite link."""
    if re.search(r"discord(app)?\.(com/invite|gg)/[a-zA-Z0-9]", message.content):
        return "invite links are not allowed"


MESSAGE_FILTERS = [invite_link]
