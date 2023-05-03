import discord
from discord.ext import commands
from discord.utils import get

from parse import video_search

intents = discord.Intents.default()
intents.members = True
intents.messages = True

bot = commands.Bot(command_prefix=config['prefix'], description=config['description'], intents=intents)


# ---------------------------------- #
#            Cfg commands            #
# ---------------------------------- #
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    
    channel = bot.get_channel(1059558767575965767)
    await channel.send('Бот запущен')


@bot.command()
@commands.has_role('Staffㆍᔪ👑ᔨ')
async def cfg(ctx):
    await ctx.send('What`s up?')


@bot.command()
@commands.has_role('Staffㆍᔪ👑ᔨ')
async def sendreact(ctx, channel):
    rule = bot.get_channel(927592400753422413)
    game = bot.get_channel(927592401130881068)
    
    if channel == 'rule':
        await rule.send('Вы ознакомились со всеми правилами?')
    elif channel == 'game':
        await game.send('Здесь вы можете выбрать игры, с игроками которых вы бы хотели общаться')
    elif channel == 'all':
        await rule.send('Вы ознакомились со всеми правилами?')
        await game.send('Здесь вы можете выбрать игры, с игроками которых вы бы хотели общаться')


# ---------------------------------- #
#         Reactions commands         #
# ---------------------------------- #
@bot.event
async def on_reaction_add(reaction, user):
    emoji = reaction.emoji
    print(emoji)
    
    if reaction.message.channel.id == 927592400753422413 and emoji == "👍":  # rule channel
        role = discord.utils.get(user.guild.roles, id=927592400736636930)
        await user.add_roles(role)
    
    elif reaction.message.channel.id == 927592401130881068 and str(emoji) in roles:  # game channel
        role = discord.utils.get(user.guild.roles, id=roles[str(emoji)])
        await user.add_roles(role)


@bot.event
async def on_reaction_remove(reaction, user):
    emoji = reaction.emoji
    print(emoji)
    
    if reaction.message.channel.id == 927592401130881068 and str(emoji) in roles:
        role = discord.utils.get(user.guild.roles, id=roles[str(emoji)])
        await user.remove_roles(role)


# ---------------------------------- #
#           Music commands           #
# ---------------------------------- #
@bot.command()
@commands.has_role('dj')
async def join(ctx, *name):
    name = ' '.join(list(name))
    url = video_search(name)
    
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    
    if voice and voice.is_connected():
        voice = await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")
    
    voice.play(discord.FFmpegPCMAudio(executable="ffapps/ffmpeg.exe", source='1.mp3'))


@bot.command()
@commands.has_role('dj')
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    
    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left {channel}")
        await ctx.send(f"Left {channel}")
    else:
        print("Bot was told to leave voice channel, but was not in one")
        await ctx.send("Don't think I am in a voice channel")


if __name__ == '__main__':
    bot.run(config['token'])
