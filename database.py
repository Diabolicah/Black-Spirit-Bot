import player_class as pclass, guild_class as gclass
import config as c


class Database:
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(Database(bot))


def set_player_data(user, player):
    """Updates/Creates user player data."""
    if c.player_collection.find_one({"_id": user.id}) is None:
        c.player_collection.insert_one({"_id": user.id})
    for player_data in player.__dict__:
        if "character" not in player_data:
            c.player_collection.find_one_and_update({"_id": user.id}, {"$set": {player_data: player.__dict__[player_data]}})
    for character_slot in range(c.player_character_slots):
        character = "character_{0}".format(character_slot)
        c.player_collection.find_one_and_update({"_id": user.id}, {"$set": {character: player.characters[character_slot].__dict__}})


def get_player_data(user):
    """Retrurns user player data."""
    data = c.player_collection.find_one({"_id": user.id})
    if data is None:
        set_player_data(user, pclass.PlayerClass())
        data = c.player_collection.find_one({"_id": user.id})
    player = pclass.PlayerClass()
    for player_data in data:
        if "character" not in player_data:
            player.__dict__[player_data] = data[player_data]
    for character_slot in range(c.player_character_slots):
        character = "character_" + str(character_slot)
        for character_data in data[character]:
            player.characters[character_slot].__dict__[character_data] = data[character][character_data]
    return player


def create_guild_data(guild):
    if c.guild_collection.find_one({"name": guild.name}) is None:
        nguild = gclass.GuildClass(name=guild.name, guild_master_id=guild.guild_master_id)
        c.guild_collection.insert_one(nguild.__dict__)
        return True
    else:
        return False


def set_guild_data(guild):
    """Updates guild data."""
    if c.guild_collection.find_one({"name": guild.name}) is None:
        return False
    c.guild_collection.find_one_and_update({"name": guild.name}, {"$set": guild.__dict__})


def get_guild_data(guild_name):
    """Retrurns guild data."""
    data = c.guild_collection.find_one({"name": guild_name})
    if data is None:
        return
    guild = gclass.GuildClass()
    for guild_data in data:
        guild.__dict__[guild_data] = data[guild_data]
    return guild
