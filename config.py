import os
import pymongo

class Config:
    def __init__(self, bot):
        self.bot = bot


# discord variables
prefix = "*"
token = "NDE1NDk3ODU1MDMwMTMyNzM2.DahF8Q.40tC4sRHVGP9uIyUDQ0afdXKDls"
bot_owner_id = "133022153405628416"
delete_timer = 1
task_timer = 300
default_misc_color = 0xad46f2
default_attendance_color = 0xe5f442
dev_server_id = "410147102384062464"
server_log_channel_id = "410147217416912897"

# bdo variables
player_character_slots = 15
player_character_classes = ["warrior", "ranger", "sorceress", "berserker", "valkyrie", "wizard", "witch", "tamer", "maehwa", "musa", "ninja", "kunoichi", "dark_knight", "striker", "mystic"]
guild_max_size = 100
image_directory = os.getcwd()+"/Images/"
guild_max_attendance = 5

# database variables
connection = pymongo.MongoClient("mongodb://localhost")
database = connection.blackspiritdatabase
server_collection = database.servers
guild_collection = database.guilds
player_collection = database.players
attendance_collection = database.attendance

def setup(bot):
    bot.add_cog(Config(bot))

