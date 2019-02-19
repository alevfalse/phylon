import config

async def sendCommands(ctx):
    string =  '**Commands [{}]**\n'.format(config.prefix)
    string += '- cmd - Sends this list.\n'
    string += '- get `<snippet id>` - Retrieve a snippet from the database using its id.\n'
    string += '- save `<snippet title> <snippet content>` - Save a snippet into the database.\n'
    string += '- getAll - Lists all snippets saved in the database.\n'
    string += '- edit <snippet id> - Delete a snippet from the database using its id.\n'
    string += '- delete <snippet id> - Edit a snippet\'s content using its id.\n'
    string += '- say `<message>` - Makes the bot say something.\n'
    string += '- shutdown - Logs out the bot and exits the script.\n'
    string += '- toss - Toss a coin.\n'

    await ctx.send(string)