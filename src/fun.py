import random
import requests

async def TossCoin(ctx):
    number = random.randint(0,1)
    print(number)

    if number == 1:
        await ctx.send('Head!')
    else:
        await ctx.send('Tail!')

async def Chat(message):

    askload = {
        'user': 'Pdfu3Nhlleco3YVA',
        'key': 'oFVi3hcOv7QXTherbQweVM2C8mErLzKv',
        'nick': 'Phylon',
        'text': message.content
    }

    try:
        await message.channel.trigger_typing()
        r = requests.post('https://cleverbot.io/1.0/ask', data=askload)
        print(r.json())
        data = r.json()
        await message.channel.send(data['response'])
    except Exception as e:
        print(e)
        await message.channel.send(e)