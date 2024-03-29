import discord
from discord.ext import commands
import random
import os 


def start_bot(client, token):

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            client.load_extension(f'cogs.{filename[:-3]}')

    @client.event
    async def on_ready():
        print('Bot is online.')
        await client.change_presence(status=discord.Status.idle, activity=discord.Game('Alvin so fat yuh'), owner_id=252127360063766529)

    client.run(token)
    

def main():
    client = commands.Bot(command_prefix='$', case_insensitive=True)
    token = TOKEN
    start_bot(client, token)

if __name__ == "__main__":
    main()  
