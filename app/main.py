import asyncio
import discord
from discord.ext import tasks
from modules.common import Common
from modules.alpaca import AlpacaLib

client = discord.Client()
alpaca_config = Common().get_secret_info('alpaca-test')
alpaca = AlpacaLib(
    endpoint=alpaca_config['endpoint'],
    keyid=alpaca_config['keyid'],
    secret=alpaca_config['secret']
)
token = Common().get_secret_info('discord')
token = token['token']
listofstonks = ['SPY','GME','NOK','AMC']
current_stock_index = 0

async def change_presence():
    while True:
        try:
            #print(f"Running loop")
            global current_stock_index
            global listofstonks
            current_stock_symbol = listofstonks[current_stock_index]
            current_stock_price = alpaca.get_stock_price(current_stock_symbol)
            stock_str = f"{current_stock_symbol}: {current_stock_price}"
            await client.change_presence(
                activity=discord.Activity(type=discord.ActivityType.watching, name=stock_str)
            )
            if len(listofstonks) - 1 < current_stock_index + 1:
                current_stock_index = 0
            else:
                current_stock_index += 1
            await asyncio.sleep(30)
        except Exception as e:
            print(e)
            await asyncio.sleep(30)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    client.loop.create_task(change_presence())

client.run(token)