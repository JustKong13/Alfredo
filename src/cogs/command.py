import discord
from discord.ext import commands
import random
import os
import json


class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
        
    @commands.command(name='8ball', help="Ask me a question!")
    async def _8ball(self, ctx, question):
        pred = [
                "It is certain.",
                "It is decidedly so.",
                "Without a doubt.",
                "Yes - definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "Most likely.",
                "Outlook good.",
                "Yes.",
                "Signs point to yes.",
                "Reply hazy, try again.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don't count on it.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful."
            ]
        await ctx.channel.send(random.choice(pred))

    @_8ball.error
    async def _8ball_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send("Alfredo has nothing to answer. Please provide a question.")

    @commands.command(aliases=["bae-suzy", 'baesuzy'], help="Random Bae Suzy photo")
    async def bae_suzy(self, ctx):
        bae_suzy = [filename for filename in os.listdir('bae_suzy')]
        await ctx.channel.send(file=discord.File('bae_suzy/' + str(random.choice(bae_suzy))))

    @commands.command(help="View a player's opgg")
    async def opgg(self, ctx, *,ign):
        ign = ign.replace(' ', '%20')
        await ctx.channel.send('https://na.op.gg/summoner/userName='+str(ign)) 

    @opgg.error 
    async def opgg_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send("Please provide a player IGN.")

    @commands.command()
    async def tsm(self, ctx):
        tsm_file = [filename for filename in os.listdir('tsm')]
        await ctx.channel.send(file=discord.File('tsm/' + str(random.choice(tsm_file))))

    @commands.command()
    async def roll(self, ctx, i, j):
        i = int(i)
        j = int(j)
        value = random.randint(i, j)
        await ctx.channel.send(str(value))

    @roll.error
    async def roll_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send("Please provide a minimum and maximum number.")
        else:
            await ctx.channel.send("Sorry Alfredo does not understand your number. Please make sure you follow these requirements: \n - Are your numbers integers?\n - Is the first number smaller than your second number? \n - Did you make sure to follow this format: $random <first number> <second number>")
        
    @commands.command()
    async def test(self, ctx):
        if self.client.latency < 0.08:
            await ctx.channel.send(f'Alfredo bot is running at {self.client.latency * 1000}ms.')
        else:
            await ctx.channel.send(f'Alfredo bot is running at {self.client.latency * 1000}ms. GOD DAMN WE LAGGING LAGGING')

    @commands.command()
    @commands.has_guild_permissions(manage_messages=True)
    async def list_command(self, ctx, *, text, help="Lists out Alfredo responses to key words"):
        with open('events.json') as f:
            json_open = json.load(f)

        found = False
        for event_dict in json_open['commands']:
            if text == event_dict['input']:
                response = ""
                for i in range(len(event_dict['output'])):
                    response += " " + event_dict['output'][i] + ','
                await ctx.channel.send(response[:-1])
                found = True
        if found == False:
            await ctx.channel.send('Your command was not found. You can add this command using $add_command {} <output>.'.format(text))

    @list_command.error
    async def list_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            with open('events.json') as f:
                json_open = json.load(f)
            
            response = ""
            for event_dict in json_open["commands"]:
                response += "\n - " + event_dict['input'] + ' ' 
            await ctx.channel.send("This is what I respond to: " + response)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.channel.send("That command doesn't appear to exist. Use $help for help.") 

def setup(client):
    client.add_cog(Command(client))