from datetime import datetime

import disnake
from disnake import Embed

from . import get_config

cfg = get_config()

class obyn_embed(Embed):
    """" Custom Embed class for Obyn bots. """
    def __init__(self, author: disnake.User | disnake.Member | disnake.ClientUser):
        super().__init__()
        self.set_author(
            name=author.name,
            icon_url=author.display_avatar,
        )
        self.color = int(cfg["embed_color"], 16)
        self.timestamp = datetime.now()
        self.set_footer(
            text=f"User ID: {author.id}",
            icon_url=author.display_avatar
        )
