import discord
import os

from discord import message
from scraper import scrapeEast, scrapeServerStatus
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
east_servers = {}

bot = commands.Bot(command_prefix='~', help_command=None)

# Collects online status of all US East servers every 2 minutes
# If the tracked server is 
@tasks.loop(minutes=2)
async def scrape():
    global call_counter
    global server_status # tracked server status
    global server_name # tracked server
    global global_ctx
    global east_servers
    status_dict = scrapeEast()
    if len(server_name) > 1:
        if (status_dict[server_name] == server_status):
            pass
        else:
            server_status = status_dict[server_name]
            if (global_ctx != None):
                await global_ctx.send(status_dict[server_name])
    east_servers = status_dict

# Reports a server's status, but does not track it
@bot.command(name='check')
async def check_server(ctx, arg):
    server_status = scrapeServerStatus(arg)
    await ctx.send(server_status)

# sets a tracked server to get updates on
# will post updates in the channel where the command was used
@bot.command(name="track")
async def set_server(ctx, arg):
    global server_name
    global global_ctx
    global_ctx = ctx
    server_name = arg
    server_status = scrapeServerStatus(arg)
    await ctx.send('Now tracking ' + arg + '. Current status: ' + server_status)

# Message with the status of the last tracked server
# if a server is provided, call the set command instead
@bot.command(name='status')
async def get_status(ctx, arg=None):
    global server_status
    global server_name
    global global_ctx
    global_ctx = ctx
    if arg != None:
        set_server(ctx, arg)
    else:
        if server_name == '':
            await ctx.send('No tracked server. Use \"~track [Server Name]\" or \"~status [Server Name]\" to start tracking a server.')
        else:
            await ctx.send(server_status)

@bot.command(name='help')
async def help_user(ctx):
    helpString = '```Commands:\n\t\"~track [Server Name]\": Set a server to track the status of. If it changes, I will (probably) report it!\n'
    helpString += '\t\"~check [Server Name]\": Check the status of a server. This will not start tracking this server.\n'
    helpString += '\t\"~status\": Get the status of the currently tracked server. Providing a server name will also start tracking that server.```'
    await ctx.send(helpString)

scrape.start()
from dotenv import load_dotenv
load_dotenv()
bot.run(os.environ["TOKEN"])

