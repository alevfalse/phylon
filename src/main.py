from dotenv import load_dotenv
load_dotenv(verbose=True)

import os
import sys
import discord
import logging
from discord.ext import commands

# my modules
import config
import database
import functions
import fun

logging.basicConfig(level=logging.INFO)

Bot = commands.Bot(command_prefix=config.prefix, description=config.description)
Bot.owner_id = config.OwnerID

# EVENTS =========================================================================
@Bot.event
async def on_ready():
    '''When the bot starts up.'''
    logging.info('{} reporting for duty!'.format(Bot.user.display_name))

@Bot.event
async def on_command_error(ctx, error):
    '''When a command error occurs'''
    await ctx.send(error)

@Bot.event
async def on_message(message):
    await Bot.process_commands(message)
    if (message.channel.id == config.ChatChannelID):
        await fun.Chat(message)

# COMMANDS =========================================================================
@Bot.command()
async def get(ctx, id):
    '''Get a code snippet using its id.'''
    await database.get(ctx, id)

@Bot.command()
async def save(ctx, title, *, snippet):
    '''Save a string into the database with title.'''
    await database.save(ctx, title, snippet)

@Bot.command()
async def getall(ctx):
    '''Lists all code snippets saved in the database by id, title and author.'''
    await database.getall(ctx)

@Bot.command()
async def edit(ctx, id):
    '''Update a snippet using its id.'''
    await database.edit(ctx, id)

@Bot.command()
async def delete(ctx, id):
    '''Delete a snippet using its id.'''
    await database.delete(ctx, id)

# FOR FUN ========================================================================
@Bot.command()
async def say(ctx, *, text):
    '''Make the bot say something.'''
    await ctx.message.delete()
    await ctx.send(text)

@Bot.command()
async def toss(ctx):
    '''Toss a coin.'''
    await fun.TossCoin(ctx)

# MISC =============================================================================
@Bot.command()
async def cmd(ctx):
    '''Posts all available commands.'''
    await functions.sendCommands(ctx)

@Bot.command()
async def shutdown(ctx):
    '''Logs out the bot and exits the script.'''
    await ctx.send('Shutting down...')
    sys.exit('Shutdown by {}'.format(ctx.author.display_name))

# LOGIN
if os.getenv('TOKEN'):
    Bot.run(os.getenv('TOKEN'))
else:
    logging.error('No TOKEN found in environment variables.')

