import discord
import config as c


class GuildClassCog:
    def __init__(self, bot):
        self.bot = bot


class GuildClass:
    def __init__(self, name="", server_id="", guild_master_id="", officer_role="Officer", member_role="Member", description="This is a guild description.", show_avg=True, recruiting=False,
                 recruitment_message="This is a recruitment message.", attendance_message=""):
        """Guild Constructor"""
        self.name = name
        self.server_id = server_id
        self.guild_master_id = guild_master_id
        self.officer_role = officer_role
        self.member_role = member_role
        self.description = description
        self.show_avg = show_avg
        self.recruiting = recruiting
        self.recruitment_message = recruitment_message
        self.attendance_message = attendance_message

    def get_logo(self):
        pass

    def get_member_count(self):
        temp = c.player_collection.find({"guild": self.name})
        return temp.count()

    def get_avg_guildscore(self):
        temp = c.player_collection.find({"guild": self.name})
        avg = 0
        for doc in temp:
            avg = avg + doc["character_0"]["character_dp"] + (doc["character_0"]["character_ap"] if int(doc["character_0"]["character_ap"]) > doc["character_0"]["character_awakening"] else doc["character_0"]["character_awakening"])
        avg = avg / temp.count()
        return avg

    def embed_guild(self, bot):
        """Returns an embed object of the guild data."""
        try:
            user = bot.get_server(id=c.dev_server_id).get_member(user_id=self.guild_master_id)
            guild_embed = discord.Embed(title="Guild Master: {0}".format(user.name if user is not None else "Unknown"), description=self.description, colour=c.default_misc_color)
            guild_embed.set_author(name="{0}'s Guild ID Card".format(self.name))
            guild_embed.add_field(name="Members", value="{0}/{1}".format(self.get_member_count(), c.guild_max_size), inline=False)
            if self.show_avg:
                guild_embed.add_field(name="Avg Gear Score", value="{0}".format(self.get_avg_guildscore(), c.guild_max_size), inline=False)
        except Exception:
            pass
        return guild_embed

def setup(bot):
    bot.add_cog(GuildClassCog(bot))
