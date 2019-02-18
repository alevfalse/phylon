from dotenv import load_dotenv
load_dotenv(verbose=True)

import os
import discord
import logging
from discord.ext import commands

# my modules
import config
import database
import functions

logging.basicConfig(level=logging.INFO)

Bot = commands.Bot(command_prefix=config.prefix, description=config.description)
Bot.owner_id = config.OwnerID

@Bot.event
async def on_ready():
    '''When the bot starts up.'''
    logging.info('{} reporting for duty!'.format(Bot.user.display_name))


# COMMANDS =========================================================================
@Bot.command()
async def say(ctx, *, text):
    '''Make the bot say something.'''
    await ctx.message.delete()
    await ctx.send(text)

@Bot.command()
async def evaluate(ctx, *, code):
    '''Evaluate a python code\'s syntax.'''
    await functions.evaluateCode(ctx, code)

@Bot.command()
async def saveCode(ctx, title, *, code):
    '''Save a string into the database with title.'''
    await database.saveCode(ctx, title, code)

@Bot.command()
async def getCode(ctx, title):
    '''Get a code snippet using its title.'''
    await database.getCode(ctx, title)

@Bot.command()
async def listCodes(ctx):
    '''Lists all code snippets saved in the database by title and author.'''
    await database.listCodes(ctx)

if os.getenv('TOKEN'):
    Bot.run(os.getenv('TOKEN'))
else:
    logging.error('No TOKEN found in environment variables.')

