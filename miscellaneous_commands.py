"""Misc. Commands"""
import discord
from discord.ext import commands
import config as c


class MiscellaneousCommands:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["inv"], description="Command to invite the bot to your own discord.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def invite(self):
        """Whispers an invite link of bot.

        This command whispers you an invite link of the bot.

        Usage: Invite
        """
        invite_embed = discord.Embed(title="Invite Link", description="https://discordapp.com/oauth2/authorize?client_id={0}&scope=bot&permissions=8".format(self.bot.user.id),  color=c.default_misc_color)
        await self.bot.whisper(embed=invite_embed)

    @commands.command(description="Command to get an invite to the development server.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def server(self):
        """Whispers an invite link of development server.

        This command whispers you an invite link of the bot development server.

        Usage: Server
        """
        invite_embed = discord.Embed(title="Invite Link", description="https://discord.gg/e5dTtSR".format(self.bot.user.id), color=c.default_misc_color)
        await self.bot.whisper(embed=invite_embed)



def setup(bot):
    bot.add_cog(MiscellaneousCommands(bot))
