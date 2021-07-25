import discord
import os

from discord import message
from scraper import scrapeServerStatus
from discord.ext import commands, tasks

# class MyClient(discord.Client):
#     async def on_ready(self):
#         print(f'Logged in as {self.user} (ID: {self.user.id})')
#         print('------')

#     async def on_message(self, message):
#         # we do not want the bot to reply to itself
#         if message.author.id == self.user.id:
#             return

#         if message.content.startswith('!hello'):
#             await message.reply('Hello!', mention_author=True)
        
#         if message.content.startswith('!status'):
#             await message.reply(str(scrapeServerStatus()))

#     @tasks.loop(seconds=5.0)
#     async def scrape():
#         message.send(str(scrapeServerStatus()))

# client = MyClient()
###
call_counter = 0
server_status = ''
server_name = ''
global_ctx = None

bot = commands.Bot(command_prefix='~')

@tasks.loop(minutes=1)
async def scrape():
    global call_counter
    global server_status
    global server_name
    global global_ctx
    if len(server_name) == 0:
        server_name = 'Atlantis'
    status = scrapeServerStatus(server_name)
    if (status == server_status):
        pass
    else:
        server_status = status
        if (global_ctx != None):
            await global_ctx.send(status)

# @bot.command(name='status')
# async def get_status(ctx, arg):
#     global server_status
#     global server_name
#     if server_name != arg:
#         server_name = arg
#         server_status = scrapeServerStatus(arg)
#     await ctx.send(server_status)

@bot.command(name="set")
async def set_server(ctx, arg):
    global server_name
    global global_ctx
    global_ctx = ctx
    server_name = arg
    server_status = scrapeServerStatus(arg)
    await ctx.send('Now tracking ' + arg + '. Current status: ' + server_status)

# Message with the status of the last tracked server
@bot.command(name='status')
async def get_status(ctx, arg=None):
    global server_status
    global server_name
    global global_ctx
    global_ctx = ctx
    await ctx.send(server_status)

# @bot.command(name='track')
# async def start_tracking(ctx):


scrape.start()
from dotenv import load_dotenv
load_dotenv()
bot.run(os.environ["TOKEN"])

