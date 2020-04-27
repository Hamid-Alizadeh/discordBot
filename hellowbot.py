import asyncio
import discord
import pickle
import json
from discord.ext import commands, tasks
from itertools import cycle
import os
import random
from threading import Timer

client = commands.Bot(command_prefix='.')
here = os.path.dirname(os.path.abspath(__file__))
invitation = "https://discordapp.com/api/oauth2/authorize?client_id=697364476504309780&scope=bot"
status = cycle(['Status 1', 'Status 2'])


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command used.")
    pass


@client.event
async def on_ready():
    change_status.start()
    # unload('mafia')
    print('Logged on as {client.user}!')


# @client.event
# async def on_message(message):
#     author = message.author
#     content = message.content
#     channel = message.channel
#     # message.content == message.content.lower()
#     if author != client.user:
#         print('{}: {} in channel: {}'.format(author, content, channel))
#         # await message.channel.send('{}: {}'.format(channel, content))
#         await client.process_commands(message)


@client.command(aliases=['8ball', 'test'])
async def _8ball(ctx, *, question):
    roles = ['Mafia',
             'Godfather',
             'Detective',
             'Doctor',
             'Spy',
             'Robinhood',
             ]
    try:
        await ctx.send(f'Question: {question}\nAnswer:{random.choice(roles)}')
    except:
        print('somthing')


@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')


# @client.command()
# async def slap(ctx, members: commands.Greedy[discord.Member], *, reason='no reason'):
#     slapped = ", ".join(x.name for x in members)
#     await ctx.send('{} just got slapped for {}'.format(slapped, reason))
#
# @client.command()
# async def welcome(ctx):
#     await ctx.send('lotfan berin be chanele ')
#     load_lobby = pickle.load(open("game_lobby.p", "rb"))
#     for p_id, p_info in lobby.items():
#         print(p_info['role'])
#     game = {'set': load_lobby, 'nights': 1}
#     # game_is_running: bool = True
#
#     print(lobby)
#     embed = discord.Embed(
#         title='خوش آمدید',
#         description=str(len(lobby)) + "شهروند جدید به شهر شیراز وارد شدند\n شب" + game['nights'],
#         colour=discord.Colour.dark_green()
#     )
#     embed.set_thumbnail(
#         url='https://www.pngrepo.com/png/49762/180/city-hall.png')
#     for p_id, p_info in lobby.items():
#         player = str(p_info['name'])
#         embed.add_field(name=player, value='شهروند', inline=False)
#     print(game)
#     await ctx.send(embed=embed)


@client.command()
async def dust(ctx):
    t = Timer(5.0, nasu)
    t.start()
    await ctx.send("GHatab mamjow nasu dust.")


# @client.event
# async def on_message(message):
#     if message.content.startswith('$thumb'):
#         channel = message.channel
#         await channel.send('Send me that 👍 reaction, mate')
#
#         def check(reaction, user):
#             return user == message.author and str(reaction.emoji) == '👍'
#
#         try:
#             reaction, user = await client.wait_for('reaction_add', timeout=5.0)
#             await channel.send(str(reaction))
#         except asyncio.TimeoutError:
#             await channel.send('👎')
#         else:
#             await channel.send('👍')
#
def nasu():
    print("test")


@client.command()
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("please specify an amount of messages to delete.")


@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


if __name__ == '__main__':

    token = 'Njk3MzY0NDc2NTA0MzA5Nzgw.Xo2O6g.ir9TEoZZgkpFRQDE52JnMjfBlOM'
    client.run(token)
