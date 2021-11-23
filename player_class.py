import character_class as cclass
import config as config
import discord


class PlayerClassCog:
    def __init__(self, bot):
        self.bot = bot


class PlayerClass:
    def __init__(self, family_name="", guild="", guild_rank="", guild_invite="", trina_axe=-1, allow_show_everyone=False, response="---"):
        """Player Constructor."""
        self.family_name = family_name
        self.guild = guild
        self.guild_rank = guild_rank
        self.guild_invite = guild_invite
        self.trina_axe = trina_axe
        self.allow_show_everyone = allow_show_everyone
        self.response = response
        self.characters = [cclass.CharacterClass() for _ in range(config.player_character_slots)]

    def swap_characters(self, character1, character2):
        """Swaps positions between two characters."""
        self.characters[character1],  self.characters[character2] = self.characters[character2],  self.characters[character1]

    def embed_character(self, position):
        """Returns an embed object of the character data."""
        character = self.characters[position]
        character_embed = discord.Embed(title="Character: " + character.character_name, description="", color=config.default_misc_color)
        character_embed.add_field(name="Class", value=character.character_class if character.character_class != "" else "­", inline=True)
        character_embed.add_field(name="Level", value=str(character.character_level), inline=True)
        character_embed.add_field(name="Awakening AP", value=str(character.character_awakening), inline=False)
        character_embed.add_field(name="AP", value="{0} ({1})".format(character.character_ap, character.calculated_ap()), inline=True)
        character_embed.add_field(name="DP", value="{0} ({1})".format(character.character_dp, character.calculated_dp()), inline=True)
        character_embed.add_field(name="Trina Axe", value=self.trina_axe, inline=True)
        character_embed.set_footer(text="{0} | GearScore = {1} | Fame = {2} | {3}/{4}".format(self.family_name, character.gear_score(), character.fame(), position + 1, config.player_character_slots))
        return character_embed

    def is_officer(self, guild):
        if self.guild == "":
            return False
        if self.guild_rank != guild.officer_role:
            return False
        return True

    def can_affect(self, player, guild):
        if self.guild != player.guild or (not self.is_officer(guild) and self.guild == player.guild):
            return False
        return True

def setup(bot):
    bot.add_cog(PlayerClassCog(bot))
