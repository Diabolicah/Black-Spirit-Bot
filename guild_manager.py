import database as db
import config as c
import player_class as pclass
import guild_class as gclass
import asyncio

class GuildManager:
    def __init__(self, bot):
        self.bot = bot

    def get_guild(self, player):
        if player.guild == "":
            return
        return db.get_guild_data(player.guild)

def setup(bot):
    bot.add_cog(GuildManager(bot))
