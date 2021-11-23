"""Misc. Commands"""
from discord.ext import commands
import discord
import config as c, database as db
import guild_class as gclass
import asyncio
import urllib.request
import datetime


class BlackDesertOnlineCommands:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True, description="Command to check player character data.")
    async def stats(self, ctx):
        """Stats manipulation command

        This command allows you to check your own characters data if used without sub command.

        Usage: Stats [<slot>] [mention]
        """
        if ctx.invoked_subcommand is None:
            mentions = ctx.message.mentions
            command_list = ctx.message.content.split(" ")
            for i in mentions:
                command_list.remove(i.mention)

            if len(mentions) > 0:
                target = mentions[0]
                player = db.get_player_data(mentions[0])
                issuer = db.get_player_data(ctx.message.author)
                if not issuer.can_affect(player, db.get_guild_data(issuer.guild)):
                    if not player.allow_show_everyone:
                        await self.bot.whisper("Can not check other's stats!")
                        return
            else:
                target = ctx.message.author
                player = db.get_player_data(ctx.message.author)
            invisible_channel = self.bot.get_server(id=c.dev_server_id).get_channel(channel_id=c.server_log_channel_id)
            try:
                if len(command_list) == 2 and command_list[1].isdigit() and 1 <= int(command_list[1]) <= 15:
                    character_embed = player.embed_character(int(command_list[1])-1).set_author(name="{0}{1}'s character".format("[{0}]".format(player.guild if player.guild != "" else ""), target.name)).set_thumbnail(url=target.avatar_url)
                    message = await self.bot.send_file(invisible_channel, c.image_directory + str(target.id) + "_{0}{1}".format(int(command_list[1])-1, ".png"))
                    character_embed.set_image(url=message.attachments[0]["url"])
                else:
                    character_embed = player.embed_character(0).set_author(name="[{0}] {1}'s character".format(player.guild, target.name)).set_thumbnail(url=target.avatar_url)
                    message = await self.bot.send_file(invisible_channel,  c.image_directory + str(target.id) + "_{0}{1}".format(0, ".png"))
                    character_embed.set_image(url=message.attachments[0]["url"])
            except Exception:
                pass
            await self.bot.whisper(embed=character_embed)

    @stats.command(name="show", pass_context=True, description="Command to show player character data in channel.")
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def stats_show(self, ctx):
        """Show character data.

        This command allows you to show your own characters data in the current channel.

        Usage: Stats show [<slot>] [mention]
        """
        mentions = ctx.message.mentions
        command_list = ctx.message.content.split(" ")
        for i in mentions:
            command_list.remove(i.mention)

        if len(mentions) > 0:
            target = mentions[0]
            player = db.get_player_data(mentions[0])
            issuer = db.get_player_data(ctx.message.author)
            if not issuer.can_affect(player, db.get_guild_data(issuer.guild)):
                if not player.allow_show_everyone:
                    await self.bot.say("Can not show others stats!", delete_after=c.delete_timer)
                    return
        else:
            target = ctx.message.author
            player = db.get_player_data(ctx.message.author)
        invisible_channel = self.bot.get_server(c.dev_server_id).get_channel(c.server_log_channel_id)
        try:
            if len(command_list) == 3 and command_list[2].isdigit() and 1 <= int(command_list[2]) <= 15:
                character_embed = player.embed_character(int(command_list[2]) - 1).set_author(name="{0} {1}'s character".format("[{0}]".format(player.guild if player.guild != "" else ""), target.name)).set_thumbnail(url=target.avatar_url)
                message = await self.bot.send_file(invisible_channel, c.image_directory + str(target.id) + "_{0}{1}".format(int(command_list[2]) - 1, ".png"))
                character_embed.set_image(url=message.attachments[0]["url"])
            else:
                character_embed = player.embed_character(0).set_author(name="[{0}] {1}'s character".format(player.guild, target.name)).set_thumbnail(url=target.avatar_url)
                message = await self.bot.send_file(invisible_channel, c.image_directory + str(target.id) + "_{0}{1}".format(0, ".png"))
                character_embed.set_image(url=message.attachments[0]["url"])
        except Exception:
            pass
        await self.bot.send_typing(ctx.message.channel)
        await asyncio.sleep(1)
        await self.bot.say(embed=character_embed)

    @stats.command(name="set", pass_context=True, description="Command to update characters data.")
    async def stats_set(self, ctx):
        """Update character data.

        This command allows you to update your own characters data or your guild members characters data.

        Usage: Stats set [<slot>] <family|Name|Class|Level|AP|DP|Awakening|screenshot|Trina_Axe|Allow_Everyone_To_Check> <Value> [mention]
            Please note that Class Dark_Knight is inputted as Dark_Knight for it to register.
            Allow_Everyone_To_Check: 0=False, 1=True
        """
        try:
            mentions = ctx.message.mentions
            command_list = ctx.message.content.split(" ")
            for i in mentions:
                command_list.remove(i.mention)
            if len(mentions) > 0:
                target = mentions[0]
                player = db.get_player_data(mentions[0])
                issuer = db.get_player_data(ctx.message.author)
                if not issuer.can_affect(player, db.get_guild_data(issuer.guild)):
                    await self.bot.whisper("Can not change others stats!")
                    return
            else:
                target = ctx.message.author
                player = db.get_player_data(ctx.message.author)
            if len(command_list) == 2:
                return
            if len(command_list) >= 4 and command_list[2].isdigit() and 1 <= int(command_list[2]) <= 15:
                arg = command_list[3].lower()
                value = command_list[4]
                character_slot = int(command_list[2])
            elif len(command_list) >= 3 and command_list[2].isdigit():
                return
            else:
                arg = command_list[2].lower()
                if len(command_list) >= 4:
                    value = command_list[3]
                character_slot = 0

            if arg == "name":
                player.characters[character_slot].character_name = value
                await self.bot.whisper("Character {0} name has been changed to: {1}".format(character_slot, value))
            elif arg == "class":
                if value.lower() in c.player_character_classes:
                    player.characters[character_slot].character_class = value.lower()
                    await self.bot.whisper("Character {0} class has been changed to: {1}".format(character_slot, value))
                else:
                    await self.bot.whisper("{0} is an invalid class!".format(value))
            elif arg == "level":
                player.characters[character_slot].character_level = int(value)
                await self.bot.whisper("Character {0} level has been changed to: {1}".format(character_slot, value))
            elif arg == "ap":
                player.characters[character_slot].character_ap = int(value)
                await self.bot.whisper("Character {0} ap has been changed to: {1}".format(character_slot, value))
            elif arg == "dp":
                player.characters[character_slot].character_dp = int(value)
                await self.bot.whisper("Character {0} dp has been changed to: {1}".format(character_slot, value))
            elif arg == "awakening":
                player.characters[character_slot].character_awakening = int(value)
                await self.bot.whisper("Character {0} awakening ap has been changed to: {1}".format(character_slot, value))
            elif arg == "family":
                player.family_name = value
                await  self.bot.whisper("Family name has been changed to: {0}".format(value))
            elif arg == "screenshot":
                if len(ctx.message.attachments) == 0:
                    image_url = command_list[3]
                else:
                    image_url = ctx.message.attachments[0]["url"]
                image_filename = c.image_directory+str(target.id)+"_{0}{1}".format(character_slot, ".png")
                with urllib.request.urlopen(urllib.request.Request(image_url, headers={"User-Agent": "Magic Browser"})) as response, open(image_filename, 'wb') as image_file:
                    image_file.write(response.read())
                await self.bot.whisper("Screenshot has been updated!")
            elif arg == "trina_axe":
                player.trina_axe = int(value)
                await  self.bot.whisper("Trina axe level has been changed to: {0}".format(value))
            elif arg == "allow_everyone_to_check":
                if value == "0":
                    player.allow_show_everyone = False
                else:
                    player.allow_show_everyone = True
                await  self.bot.whisper("Everyone check your stats set to: {0}".format(player.allow_show_everyone))
            player.characters[character_slot].last_updated = datetime.datetime.now()
            db.set_player_data(target, player)
        except Exception as e:
            print(e)

    @commands.group(pass_context=True, description="Command to check guild id card.")
    async def guild(self, ctx):
        """Guild manipulation command

        This command allows you to check a guild id card if used without sub command.

        Usage: Guild <name>
        """
        if ctx.invoked_subcommand is None:
            command_list = ctx.message.content.split(" ")
            if db.get_guild_data(command_list[1]) is not None:
                guild = db.get_guild_data(command_list[1])
                guild_embed = guild.embed_guild(self.bot)
                try:
                    invisible_channel = self.bot.get_server(c.dev_server_id).get_channel(c.server_log_channel_id)
                    message = await self.bot.send_file(invisible_channel, c.image_directory + "{0}{1}".format(guild.name, ".png"))
                    guild_embed.set_thumbnail(url=message.attachments[0]["url"])
                except Exception:
                    pass
                await self.bot.whisper(embed=guild_embed)
            else:
                await self.bot.whisper("Guild doesn't exist!")

    @guild.command(name="show", pass_context=True, description="Command to show guild id card in channel.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def guild_show(self, ctx):
        """Show guild id card.

        This command allows you to show specific guild id card in the current channel.

        Usage: Guild show <Name>
        """
        command_list = ctx.message.content.split(" ")
        if db.get_guild_data(command_list[2]) is not None:
            guild = db.get_guild_data(command_list[2])
            guild_embed = guild.embed_guild(self.bot)
            try:
                invisible_channel = self.bot.get_server(c.dev_server_id).get_channel(c.server_log_channel_id)
                message = await self.bot.send_file(invisible_channel, c.image_directory + "{0}{1}".format(guild.name, ".png"))
                guild_embed.set_thumbnail(url=message.attachments[0]["url"])
            except Exception:
                pass
            await self.bot.send_typing(ctx.message.channel)
            await asyncio.sleep(1)
            await self.bot.say(embed=guild_embed)
        else:
            await self.bot.send_typing(ctx.message.channel)
            await asyncio.sleep(1)
            await self.bot.say("Guild doesn't exist!", delete_after=c.delete_timer)

    @guild.command(name="create", pass_context=True, description="Command to create a new guild.")
    @commands.check(lambda ctx: ctx.message.author.id == c.bot_owner_id)
    async def guild_create(self, ctx):
        """Create guild

        This command allows you to create a new guild with specific owner.

        Usage: Guild create <name> <mention>
        """
        command_list = ctx.message.content.split(" ")
        if c.guild_collection.find({"guild_master_id": ctx.message.mentions[0].id}).count() > 0:
            await self.bot.whisper("User already owns a guild!")
            return
        guild = gclass.GuildClass(name=command_list[2], guild_master_id=ctx.message.mentions[0].id)
        if db.create_guild_data(guild):
            player = db.get_player_data(ctx.message.mentions[0])
            player.guild = guild.name
            db.set_player_data(ctx.message.mentions[0], player)
            await self.bot.whisper("Guild: {0}, was registered with {1} as guild master!".format(guild.name, ctx.message.mentions[0].mention))
        else:
            await self.bot.whisper("Guild: {0} already exists!".format(guild.name))

    @guild.command(name="set", pass_context=True, description="Command to update guild data.")
    async def guild_set(self, ctx):
        """Update guild data.

        This command allows you to update your own guild data.

        Usage: Guild set <Server|Guild_Master|Officer_Role|Member_Role|Description|Logo|Show_Avg|Recruiting|Recruitment_Message> <Value>
            Server: This command must be used in the discord server only.
            Guild_Master: This command requires a mention in the value.
            Show_Avg: 0=False, 1=True
            Recruiting: 0=False, 1=True
        """
        command_list = ctx.message.content.split(" ")
        arg = command_list[2].lower()
        if len(command_list) > 3:
            value = command_list[3]
        player = db.get_player_data(ctx.message.author)
        guild = db.get_guild_data(player.guild)
        if ctx.message.author.id != guild.guild_master_id:
            return
        if arg == "guild_master":
            player1 = db.get_player_data(ctx.message.mentions[0])
            if guild.name == player1.guild:
                guild.guild_master_id = ctx.message.mentions[0].id
                player1.guild_rank = guild.officer_role
                db.set_player_data(ctx.message.mentions[0], player1)
                await self.bot.whisper("Guild: {0} guild master has been changed to: {1}".format(guild.name, ctx.message.mentions[0].name))
            else:
                await self.bot.whisper("Member not in guild!")
        elif arg == "server":
            guild.server_id = ctx.message.server.id
            await self.bot.whisper("Guild: {0} server has been changed to: {1}".format(guild.name, ctx.message.server.name))
        elif arg == "officer_role":
            guild.officer_role = value
            await self.bot.whisper("Guild: {0} officer role has been changed to: {1}".format(guild.name, guild.officer_role))
        elif arg == "member_role":
            guild.member_role = value
            await self.bot.whisper("Guild: {0} member role has been changed to: {1}".format(guild.name, guild.member_role))
        elif arg == "description":
            guild.description = ctx.message.content.replace(command_list[0], "", 1).replace(command_list[1], "", 1).replace(command_list[2], "", 1)
            await self.bot.whisper("Guild: {0} description has been changed to: {1}".format(guild.name, guild.description))
        elif arg == "logo":
            if len(ctx.message.attachments) == 0:
                image_url = command_list[3]
            else:
                image_url = ctx.message.attachments[0]["url"]
            image_filename = c.image_directory+"{0}{1}".format(guild.name, ".png")
            with urllib.request.urlopen(urllib.request.Request(image_url, headers={"User-Agent": "Magic Browser"})) as response, open(image_filename, 'wb') as image_file:
                image_file.write(response.read())
            await self.bot.whisper("Guild logo has been updated!")
        elif arg == "show_avg":
            if value == "0":
                guild.show_avg = False
            else:
                guild.show_avg = True
            await self.bot.whisper("Show avg on guild id card set to: {0}".format(guild.show_avg))
        elif arg == "recruiting":
            if value == "0":
                guild.recruiting = False
            else:
                guild.recruiting = True
            await self.bot.whisper("Guild shown on recruitment list set to: {0}".format(guild.recruiting))
        elif arg == "recruitment_message":
            v = ctx.message.content.replace(command_list[0], "", 1).replace(command_list[1], "", 1).replace(command_list[2], "", 1)
            if len(v) <= 300:
                guild.recruitment_message = ctx.message.content.replace(command_list[0], "", 1).replace(command_list[1], "", 1).replace(command_list[2], "", 1)
                await self.bot.whisper("Guild: {0} recruitment message has been changed to: {1}".format(guild.name, guild.recruitment_message))
            else:
                await self.bot.whisper("Guild recruitment message must be within 300 letters!")
        db.set_guild_data(guild)

    @guild.command(name="invite", pass_context = True, description="Command to invite to guild.")
    async def guild_invite(self, ctx):
        """Invite to guild.

        This command allows you to invite people to your own guild.

        Usage: Guild invite <mention>
            The user must use Guild join <guild> after you invite them, to successfully join the guild!
        """
        issuer = ctx.message.author
        player = db.get_player_data(issuer)
        if player.guild != "":
            guild = db.get_guild_data(player.guild)
            if player.is_officer(guild):
                user = ctx.message.mentions[0]
                player = db.get_player_data(user)
                player.guild_invite = guild.name
                db.set_player_data(user ,player)
                await self.bot.whisper("Invitation sent successfully!")
                await self.bot.send_message(user, "You received a \"{0}\" guild invitation from: {1}, \n Type *guild join {0} to accept the invitation!".format(guild.name, ctx.message.author.mention))
            else:
                await self.bot.whisper("You must be an officer in the guild!")
        else:
            await self.bot.whisper("You must be in a guild!")

    @guild.command(name="join", pass_context=True, description="Command to accept guild invitation.")
    async def guild_join(self, ctx):
        """Accept a guild invitation.

        This command allows you to accept the guild invitation sent to you.

        Usage: Guild join <guild>
            The user must use Guild join <guild> after you invite them, to successfully join the guild!
        """
        command_list = ctx.message.content.split(" ")
        player = db.get_player_data(ctx.message.author)
        if db.get_guild_data(command_list[2]) is not None:
            guild = db.get_guild_data(command_list[2])
            if player.guild_invite == command_list[2] or guild.guild_master_id == ctx.message.author.id:
                player.guild = command_list[2]
                player.guild_invite = ""
                if guild.guild_master_id == ctx.message.author.id:
                    player.guild_rank = guild.officer_role
                else:
                    player.guild_rank = guild.member_role
                db.set_player_data(ctx.message.author, player)
                await self.bot.whisper("Successfully joined {0}!".format(player.guild))
            else:
                await self.bot.whisper("You don't have an invitation to the guild: {0}".format(command_list[2]))
        else:
            await self.bot.whisper("Guild doesn't exist.")

    @guild.command(name="leave", pass_context=True, description="Command to leave a guild.")
    async def guild_leave(self, ctx):
        """Leave current guild.

        This command allows you to leave current guild.

        Usage: Guild leave
        """
        player = db.get_player_data(ctx.message.author)
        player.guild = ""
        player.guild_rank = ""
        db.set_player_data(ctx.message.author, player)
        self.bot.whisper("Successfully left the guild.")

    @guild.command(name="kick", pass_context=True, description="Command to kick a member out from guild.")
    async def guild_kick(self, ctx):
        """Kick member from guild.

        This command allows you to kick a member from the guild.

        Usage: Guild kick <mention>
        """
        user = ctx.message.mentions[0]
        player = db.get_player_data(ctx.message.author)
        player1 = db.get_player_data(user)
        if player.guild != "" and player.guild == player1.guild:
            guild = db.get_guild_data(player.guild)
            if player.is_officer(guild) and (not player1.is_officer(guild) or guild.guild_master_id == ctx.message.author.id):
                player1.guild = ""
                player1.guild_rank = ""
                db.set_player_data(user, player1)
                await self.bot.whisper("Successfully kicked {0} from the guild.".format(user))
            else:
                await self.bot.whisper("You must be an officer to kick members and member mustn't be an officer!")
        else:
            await self.bot.whisper("{0} is not in your guild.".format(user.mention))

    @guild.command(name="recruitment_list", pass_context=True, description="Command to check list of guilds recruiting members.")
    async def guild_recruitment_list(self, ctx):
        """Check recruitment list.

        This command allows you to check a list of guilds that are open for recruitment.

        Usage: Guild Recruitment_List
        """
        embed_list = discord.Embed(title="", description="", colour=c.default_misc_color)
        embed_list.set_author(name="Guilds Recruitment List")
        guilds_list = c.guild_collection.find({"recruiting": True})
        if guilds_list.count() == 0:
            await self.bot.whisper(embed=embed_list)
        number = 0
        for guild in guilds_list:
            number = number + 1
            embed_list.add_field(name=guild["name"], value=guild["recruitment_message"], inline=True)
            if number == 6:
                await self.bot.whisper(embed=embed_list)
                embed_list = discord.Embed(title="", description="", colour=c.default_misc_color)
                number = 0
        if 0 < number < 6:
            await self.bot.whisper(embed=embed_list)

    @guild.command(name="reload", pass_context=True, description="Command to reload the guild player rankings.")
    async def guild_reload(self, ctx):
        """Reload guild rankings

        This command allows you to reload the rankings of the guild members.

        Usage: Guild Reload
        """
        player = db.get_player_data(ctx.message.author)
        if player.guild !="":
            guild = db.get_guild_data(player.guild)
            if guild.guild_master_id == ctx.message.author.id:
                if guild.server_id != "":
                    server = self.bot.get_server(id=guild.server_id)
                    members = server.members
                    for member in members:
                        player1 = db.get_player_data(member)
                        temp = False
                        for role in member.roles:
                            if role.name == guild.member_role and (player1.guild == guild.name or player1.guild == "") and not temp:
                                player1.guild = guild.name
                                player1.guild_rank = guild.member_role
                            if role.name == guild.officer_role and (player1.guild == guild.name or player1.guild == ""):
                                player1.guild = guild.name
                                player1.guild_rank = guild.officer_role
                                temp = True
                        db.set_player_data(member, player1)
                    await self.bot.whisper("Successful")
                else:
                    await self.bot.whisper("Guild server must be registered!")
            else:
                await self.bot.whisper("Must be a guild owner to use this command.")
        else:
            await self.bot.whisper("Must be a guild owner to use this command.")

    @guild.command(name="leaderboard", pass_context=True, description="Command to get the guild leaderboard.")
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def guild_leaderboard(self, ctx):
        """Get guild leaderboard

        This command allows you to check the guild leaderboard ranking.

        Usage: Guild Leaderboard [show]
        """
        player = db.get_player_data(ctx.message.author)
        command_list = ctx.message.content.split(" ")
        show = False
        if len(command_list) >= 3:
            if command_list[2].lower() == "show":
                show = True
        if player.guild != "":
            guild = db.get_guild_data(player.guild)
            if guild.server_id != "":
                try:
                    server = self.bot.get_server(guild.server_id)
                    members = server.members
                    leaderboard_embed = discord.Embed(colour=c.default_misc_color, title="", description="")
                    leaderboard_embed.set_author(name="Guild Gearscore Leaderboard")
                    leaderboard_embed.set_footer(text="Avg Gearscore: {0}".format(guild.get_avg_guildscore()))
                    list = []
                    for member in members:
                        player1 = db.get_player_data(member)
                        if player1.guild == guild.name:
                            list.append(member)
                    count = 0
                    list = sorted(list, key=lambda xd: db.get_player_data(xd).characters[0].gear_score())
                    list.reverse()
                    for i in list:
                        count = count + 1
                        player = db.get_player_data(i)
                        leaderboard_embed.add_field(name="­", inline=False, value="{0}){1}: {2}".format(count, i.mention, player.characters[0].gear_score()))
                        if count%25 == 0:
                            if show:
                                await self.bot.say(embed=leaderboard_embed)
                            else:
                                await self.bot.whisper(embed=leaderboard_embed)
                            leaderboard_embed = discord.Embed(title="", description="", colour=c.default_misc_color)
                    if 0 < count%25 < 25:
                        if show:
                            await self.bot.say(embed=leaderboard_embed)
                        else:
                            await self.bot.whisper(embed=leaderboard_embed)
                except Exception as e:
                    print(e)
            else:
                await self.bot.whisper("Guild must have its server registered to use this command!")
        else:
            await self.bot.whisper("Must be in a guild to use this command!")

    @guild.command(name="list", pass_context=True, description="Command to get class specific list.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def guild_list(self, ctx):
        """Get guild class list

        This command allows you to check the class specific list.

        Usage: Guild list <class> [show]
        """
        player = db.get_player_data(ctx.message.author)
        command_list = ctx.message.content.split(" ")
        show = False
        if len(command_list) >= 4:
            if command_list[3].lower() == "show":
                show = True
        if command_list[2].lower() not in c.player_character_classes:
            await self.bot.whisper("No such class exists!")
            return

        if player.guild != "":
            guild = db.get_guild_data(player.guild)
            if guild.server_id != "":
                try:
                    server = self.bot.get_server(guild.server_id)
                    members = server.members
                    leaderboard_embed = discord.Embed(colour=c.default_misc_color, title="", description="")
                    leaderboard_embed.set_author(name="{0} Gearscore Leaderboard".format(command_list[2].title()))
                    avg = 0
                    list = []
                    for member in members:
                        player1 = db.get_player_data(member)
                        if player1.guild == guild.name and player1.characters[0].character_class.lower() == command_list[2].lower():
                            avg = avg + int(player1.characters[0].gear_score())
                            list.append(member)
                    count = 0
                    leaderboard_embed.set_footer(text="Avg Gearscore: {0}".format(avg/len(list)))
                    list = sorted(list, key=lambda xd: db.get_player_data(xd).characters[0].gear_score())
                    list.reverse()
                    for i in list:
                        count = count + 1
                        player = db.get_player_data(i)
                        leaderboard_embed.add_field(name="­", inline=True, value="{0}){1}: {2}".format(count, i.mention, player.characters[0].gear_score()))
                        if count%25 == 0:
                            if show:
                                await self.bot.say(embed=leaderboard_embed)
                            else:
                                await self.bot.whisper(embed=leaderboard_embed)
                            leaderboard_embed = discord.Embed(title="", description="", colour=c.default_misc_color)
                    if 0 < count%25 < 25:
                        if show:
                            await self.bot.say(embed=leaderboard_embed)
                        else:
                            await self.bot.whisper(embed=leaderboard_embed)
                except Exception as e:
                    print(e)
            else:
                await self.bot.whisper("Guild must have its server registered to use this command!")
        else:
            await self.bot.whisper("Must be in a guild to use this command!")

    @guild.command(name="last_updated", pass_context=True, description="Command to get last updated list.")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def guild_last_updated(self, ctx):
        """Get guild last updated list

        This command allows you to check when guild members last updated their stats!.

        Usage: Guild last_updated [show]
        """
        player = db.get_player_data(ctx.message.author)
        command_list = ctx.message.content.split(" ")
        show = False
        if len(command_list) >= 3:
            if command_list[2].lower() == "show":
                show = True
        if player.guild != "":
            guild = db.get_guild_data(player.guild)
            if guild.server_id != "":
                try:
                    server = self.bot.get_server(guild.server_id)
                    members = server.members
                    last_updated_embed = discord.Embed(colour=c.default_misc_color, title="", description="")
                    last_updated_embed.set_author(name="Guild Last Updated List")
                    list = []
                    for member in members:
                        player1 = db.get_player_data(member)
                        if player1.guild == guild.name:
                            list.append(member)
                    count = 0
                    list = sorted(list, key=lambda xd: int(db.get_player_data(xd).characters[0].last_updated.timestamp()) if db.get_player_data(xd).characters[0].last_updated != "" else 0)
                    list.reverse()
                    for i in list:
                        count = count + 1
                        if db.get_player_data(i).characters[0].last_updated != "":
                            t = datetime.timedelta(seconds=(datetime.datetime.now().timestamp() - db.get_player_data(i).characters[0].last_updated.timestamp()))
                        last_updated_embed.add_field(name="­", inline=False, value="{0}){1}: {2}".format(count, i.mention, ("{0}d {1} (h:mm:ss)".format(t.days, datetime.timedelta(seconds=t.seconds))) if db.get_player_data(i).characters[0].last_updated != "" else -1))
                        if count%25 == 0:
                            if show:
                                await self.bot.say(embed=last_updated_embed)
                            else:
                                await self.bot.whisper(embed=last_updated_embed)
                                last_updated_embed = discord.Embed(title="", description="", colour=c.default_misc_color)

                    if 0 < count%25 < 25:
                        if show:
                            await self.bot.say(embed=last_updated_embed)
                        else:
                            await self.bot.whisper(embed=last_updated_embed)
                except Exception as e:
                    print(e)
            else:
                await self.bot.whisper("Guild must have its server registered to use this command!")
        else:
            await self.bot.whisper("Must be in a guild to use this command!")

    @commands.group(pass_context=True, description="Command to check current attendance message.")
    @commands.check(lambda ctx: db.get_player_data(ctx.message.author).guild != "")
    async def attendance(self, ctx):
        """Attendanace manipulation command

        This command allows you to check current attendance if used without sub command.

        Usage: Attendance
        """
        if ctx.invoked_subcommand is None:
            user = ctx.message.author
            player = db.get_player_data(user)
            guild = db.get_guild_data(player.guild)
            attendance_embed = discord.Embed(title="", description=guild.attendance_message, colour=c.default_attendance_color)
            attendance_embed.set_author(name="Attendance Message")
            attendance_embed.set_footer(text="Use *attendance accept/decline to respond to this message!")
            await self.bot.whisper(embed=attendance_embed)

    @attendance.command(name="set", pass_context=True, description="Command to set current attendance message.")
    @commands.check(lambda ctx: db.get_guild_data(db.get_player_data(ctx.message.author).guild).officer_role == db.get_player_data(ctx.message.author).guild_rank)
    async def attendance_set(self, ctx):
        """Change attendance message

        This command allows you to set the attendance message.

        Usage: Attendance Set <message>
        """
        command_list = ctx.message.content.split(" ")
        user = ctx.message.author
        player = db.get_player_data(user)
        guild = db.get_guild_data(player.guild)
        guild.attendance_message = ctx.message.content.replace(command_list[0], "", 1).replace(command_list[1], "", 1)
        db.set_guild_data(guild)
        await self.bot.whisper("Guild attendance message set to: {0}".format(guild.attendance_message))

    @attendance.command(name="send", pass_context=True, description="Command to send current attendance message.")
    @commands.check(lambda ctx: db.get_guild_data(db.get_player_data(ctx.message.author).guild).officer_role == db.get_player_data(ctx.message.author).guild_rank)
    async def attendance_send(self, ctx):
        """Send attendance message

        This command allows you to send the attendance message.

        Usage: Attendance Send
        """
        user = ctx.message.author
        player = db.get_player_data(user)
        guild = db.get_guild_data(player.guild)
        if guild.server_id == "":
            await self.bot.whisper("Guild server must be registered!")
            return
        server = self.bot.get_server(guild.server_id)
        members = server.members
        attendance_embed = discord.Embed(title="", description=guild.attendance_message, colour=c.default_attendance_color)
        attendance_embed.set_author(name="Attendance Message")
        attendance_embed.set_footer(text="Use *attendance accept/decline to respond to this message!")

        for i in members:
            player1 = db.get_player_data(i)
            if player1.guild == guild.name:
                player1.response = "---"
                db.set_player_data(i, player1)
                try:
                    await self.bot.send_message(i, embed=attendance_embed)
                except Exception:
                    await self.bot.whisper("Couldn't send the message to: {0}, make sure they don't have the bot blocked!!".format(i.name))
                await  asyncio.sleep(5)
        await self.bot.whisper("Guild attendance message has been sent to memebers!")

    @attendance.command(name="accept", pass_context=True, description="Command to accept current attendance message.")
    async def attendance_accept(self, ctx):
        """Accept attendance message

        This command allows you to accept the attendance message.

        Usage: Attendance Accept
        """
        user = ctx.message.author
        player = db.get_player_data(user)
        player.response = "True"
        db.set_player_data(user, player)
        await self.bot.whisper("Guild attendance has been accepted!")

    @attendance.command(name="decline", pass_context=True, description="Command to decline current attendance message.")
    async def attendance_decline(self, ctx):
        """Decline attendance message

        This command allows you to decline the attendance message.

        Usage: Attendance Decline
        """
        user = ctx.message.author
        player = db.get_player_data(user)
        player.response = "False"
        db.set_player_data(user, player)
        await self.bot.whisper("Guild attendance has been declined!")

    @attendance.command(name="result", pass_context=True, description="Command to check attendance result.")
    @commands.check(lambda ctx: db.get_guild_data(db.get_player_data(ctx.message.author).guild).officer_role == db.get_player_data(ctx.message.author).guild_rank)
    async def attendance_result(self, ctx):
        """Check attendance result

        This command allows you to check current attendance result.

        Usage: Attendance result
        """
        user = ctx.message.author
        player = db.get_player_data(user)
        guild = db.get_guild_data(player.guild)
        server = self.bot.get_server(guild.server_id)
        members = server.members
        attendance_embed = discord.Embed(title="", description="", colour=c.default_attendance_color)
        attendance_embed.set_author(name="Attendance Results")

        list = []
        for i in members:
            player1 = db.get_player_data(i)
            if player1.guild == guild.name:
                list.append(i)
        count = 0
        list = sorted(list, key=lambda f: -10 if db.get_player_data(f).response == "---" else 0 if db.get_player_data(f).response == "False" else 10)
        list.reverse()
        for i in list:
            count = count + 1
            attendance_embed.add_field(name="­", inline=False, value="{0}){1}: {2}".format(count, i.mention, db.get_player_data(i).response))
            if count % 25 == 0:
                await self.bot.whisper(embed=attendance_embed)
                attendance_embed = discord.Embed(title="", description="", colour=c.default_attendance_color)
        if 0 < count % 25 < 25:
            await self.bot.whisper(embed=attendance_embed)

def setup(bot):
    bot.add_cog(BlackDesertOnlineCommands(bot))


