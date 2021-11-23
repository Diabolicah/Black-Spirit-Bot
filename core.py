"""Core of the discord bot."""
import discord
from discord.ext import commands
import asyncio
import config as c

__author__ = "Draconicah"
startup_extensions = ["config", "database", "character_class", "player_class", "guild_class","miscellaneous_commands", "black_desert_online_commands", "guild_manager"]
bot = commands.Bot(command_prefix=c.prefix, description="Black Spirit is an assistant bot to the game Black Desert Online.",pm_help=True)


# Events
@bot.event
async def on_ready():
    print('''
    +---------------------------+
    | BlackSpirit has logged in |
    +---------------------------+
    ''')
    await bot.change_presence(game=discord.Game(name='Try help command'))


@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        cd = round(error.retry_after) + 1
        message = await bot.send_message(ctx.message.channel, 'This command is on cooldown for {0:d} more second{1}.'.format(cd, 's' if cd != 1 else ''))
        await asyncio.sleep(c.delete_timer)
        try:
            await bot.delete_messages((message, ctx.message))
        except:
            pass


@bot.event
async def on_message(message):
    await process_command(message)


@bot.event
async def on_message_edit(old_message, new_message):
    if old_message.content == new_message.content: return
    await process_command(new_message)


@bot.event
async def on_member_join(member):
    pass


# Commands
@bot.command(description="Command to reload the files in the bot.")
@commands.check(lambda ctx: ctx.message.author.id == c.bot_owner_id)
async def reload():
    """Reloads the files"""
    success = True
    for extension in startup_extensions:
        print('{} has been reloaded'.format(extension))
        try:
            bot.unload_extension(extension)
            bot.load_extension(extension)
        except Exception as e:
            success = False
            await bot.whisper('Failed to load extension {0}\n{1}: {2}'.format(extension, type(e).__name__, str(e)))
    await bot.say('Commands reloaded successfully!' if success else 'Something went wrong! :sob:')


# Functions
async def process_command(message):
    if message.author == bot.user: return
    for command_line in message.content.split('\n{0}'.format(c.prefix)):
        if command_line == message.content.split('\n{0}'.format(c.prefix))[0] and not command_line.startswith(c.prefix):
            continue
        if not command_line.startswith(c.prefix):
            command_line = "{0}{1}".format(c.prefix, command_line)
        message.content = command_line
        if message.content:
            command = message.content.split()[0].replace(c.prefix, "")
            message.content = message.content.replace(command, command.lower())
            try:
                if bot.get_command(command):
                    await bot.delete_message(message)
            except:
                pass
        await bot.process_commands(message)

# async def auto_task():
#    await bot.wait_until_ready()
#    while not bot.is_closed:
#       await asyncio.sleep(c.task_timer)


if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('Failed to load extension {0}\n{1}: {2}'.format(extension, type(e).__name__, str(e)))
#    bot.loop.create_task(auto_task())
    bot.run(c.token)
