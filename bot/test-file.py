import discord
from discord.ext import commands
from discord.utils import get

from credits import config

description = 'An example bot to showcase the discord.ext.commands extension\nmodule.\nThere are a number of utility commands being showcased here.'

intents = discord.Intents.default()
intents.members = True
intents.messages = True

bot = commands.Bot(command_prefix='!', description=description, intents=intents)

message_id = '1059810235096776715'


@bot.event
async def on_message(ctx):
    global message_id
    
    if ctx.author != bot.user:
        message_id = ctx.id
        
        await ctx.reply(ctx.content)



@bot.event
async def on_reaction_add(reaction, user):
    if reaction.message.channel.id == 927592400753422413:
        print(reaction.emoji)
        if reaction.emoji == "👍":
            role = discord.utils.get(user.guild.roles, id=927592400715649025)
            await user.add_roles(role)
        elif reaction.emoji == "👎":
            role = discord.utils.get(user.guild.roles, id=927592400715649025)
            await user.remove_roles(role)


@bot.event
async def on_reaction_remove(reaction, user):
    if reaction.message.channel.id == 927592400753422413:
        print(reaction.emoji)
        if reaction.emoji == "👍":
            role = discord.utils.get(user.guild.roles, id=927592400715649025)
            await user.add_roles(role)
        elif reaction.emoji == "👎":
            role = discord.utils.get(user.guild.roles, id=927592400715649025)
            await user.remove_roles(role)





if __name__ == '__main__':
    bot.run(config['token'])
