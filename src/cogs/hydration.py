import discord 
from discord.ext import commands
import random
import time
import datetime 


class AlvinHydration(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.online = True


    @commands.command()
    async def hydrate(self, ctx):
        await ctx.channel.send("Done")
        while True: # code will only run if alvin's status is online
            if int(str(datetime.datetime.now())[11:13]) >= 8 and int(str(datetime.datetime.now())[11:13]) <= 23:
                time.sleep(random.randint(5,10)) # delay code for random period of time from 30 to 90 minutes
                recepient = await self.client.fetch_user(ctx.author.id)

                # list of all available messages
                messages = [
                    "Hi Alvin! It's time for you to drink water",
                    "Drinking time",
                    "Drinking alcohol ruins your digestive system, drinking water doesn't"
                    "It's time to drink boo",
                    "Pause what you're doing and drink some water",
                    "Drinking now allows you to maintain optimal hydration",
                    "Drink now or forever hold your peace",
                    "Four would be proud if you drunk water",
                    "Genshin is fun, but water helps you live",
                    "Drink more water",
                    "Keep calm and drink water",
                    "Water is your new best friend",
                    "Drink pure water. Stay healthy"
                ]


                await recepient.send("<@{ctx.author.id}}> " + str(random.choice(messages)))
            else:
                time.sleep(32600)



def setup(client):
    client.add_cog(AlvinHydration(client))
