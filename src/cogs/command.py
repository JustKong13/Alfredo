import discord
from discord.ext import commands
import random
import os
import json


class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
        
    @commands.command(name='8ball', help="Ask me a question!")
    async def _8ball(self, ctx, *, question):
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
        embed_var = discord.Embed(name="8 Ball",
                                  colour=400597,
                                  type='rich')
        embed_var.set_author(name="Alfredo Bot", 
                             url="https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=LucasLucas",
                             icon_url='https://static.scientificamerican.com/sciam/cache/file/ACF0A7DC-14E3-4263-93F438F6DA8CE98A_source.jpg?w=590&h=800&896FA922-DF63-4289-86E2E0A5A8D76BE1')
        embed_var.add_field(name="{}".format(question), value=random.choice(pred), inline=True)
        embed_var.set_image(url='https://img.favpng.com/7/20/18/magic-8-ball-8-ball-pool-eight-ball-clip-art-png-favpng-pVBbqBupeRZSUSYfJK5E18NGd.jpg')
        embed_var.set_footer(text="Magic 8 Ball, Wikipedia")
        await ctx.channel.send(embed=embed_var)

    @_8ball.error
    async def _8ball_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed_var = discord.Embed(colour=400597,
                                      type='rich')
            embed_var.add_field(name="ERROR", value="Alfredo has nothing to answer. Please provide a question. inline=True")
            embed_var.set_image(url='https://img.favpng.com/7/20/18/magic-8-ball-8-ball-pool-eight-ball-clip-art-png-favpng-pVBbqBupeRZSUSYfJK5E18NGd.jpg')
            embed_var.set_footer(text="Magic 8 Ball, Wikipedia")

    @commands.command(aliases=["bae-suzy", 'baesuzy'], help="Random Bae Suzy photo")
    async def bae_suzy(self, ctx):
        bae_suzy = [filename for filename in os.listdir('bae_suzy')]
        await ctx.channel.send(file=discord.File('bae_suzy/' + str(random.choice(bae_suzy))))

    @commands.command(help="View a player's opgg")
    async def opgg(self, ctx, *, ign):
        ign = ign.replace(' ', '%20')
        await ctx.channel.send('https://na.op.gg/summoner/userName='+str(ign)) 

    @opgg.error 
    async def opgg_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send("Please provide a player IGN.")

    @commands.command(help="Rolls a random number")
    async def roll(self, ctx, i, j):
        i, j = int(i), int(j)
        value = random.randint(i, j)
        await ctx.channel.send(str(value))

    @roll.error
    async def roll_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send("Please provide a minimum and maximum number.")
        else:
            await ctx.channel.send("Sorry Alfredo does not understand your number. Please make sure you follow these requirements: \n - Are your numbers integers?\n - Is the first number smaller than your second number? \n - Did you make sure to follow this format: $random <first number> <second number>")

        
    @commands.command(help='Check latency of Alfredo')
    async def test(self, ctx):
        embed_var = discord.Embed(colour=400597, 
                                  type='rich')
        embed_var.set_author(name="Alfredo Bot",
                             icon_url='https://static.scientificamerican.com/sciam/cache/file/ACF0A7DC-14E3-4263-93F438F6DA8CE98A_source.jpg?w=590&h=800&896FA922-DF63-4289-86E2E0A5A8D76BE1')
        embed_var.add_field(name="Bot is up and running", value=f'Alfredo bot is running at {self.client.latency * 1000}ms.')
        await ctx.channel.send(embed=embed_var)

    @commands.command(name='list', help="Lists out Alfredo responses to specified key words/phrases")
    @commands.has_guild_permissions()
    async def list_command(self, ctx, *, text):
        with open('events.json') as f:
            json_open = json.load(f)
        
        found = False
        for event_dict in json_open['commands']:
            if text == event_dict['input']:
                found = True
                response = ""
                for i in range(len(event_dict['output'])):
                    response += "\n{}. ".format(str(i+1)) + event_dict['output'][i]

                embed_var = discord.Embed(name="Alfredo Responses",
                                          colour=400597,
                                          type='rich')
                embed_var.set_author(name="Alfredo Bot", 
                                     url="https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=LucasLucas",
                                     icon_url='https://static.scientificamerican.com/sciam/cache/file/ACF0A7DC-14E3-4263-93F438F6DA8CE98A_source.jpg?w=590&h=800&896FA922-DF63-4289-86E2E0A5A8D76BE1')
                embed_var.add_field(name="Alfredo's responses to '{}' are:".format(text), value=response, inline=False)
                await ctx.channel.send(embed=embed_var)

        if found == False:
            response = ""
            i = 1
            for event_dict in json_open["commands"]:
                response += "\n{}. ".format(i) + event_dict['input']
                i += 1
            embed_var = discord.Embed(name="Alfredo Responses",
                                      colour=400597,
                                      type='rich')
            embed_var.set_author(name='Alfredo Bot',
                                 url="https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=LucasLucas",
                                 icon_url='https://static.scientificamerican.com/sciam/cache/file/ACF0A7DC-14E3-4263-93F438F6DA8CE98A_source.jpg?w=590&h=800&896FA922-DF63-4289-86E2E0A5A8D76BE1')
            embed_var.add_field(name="Your term was not found. This is what I respond to:", value=response, inline=False) 
            await ctx.channel.send(embed=embed_var)

    @list_command.error
    async def list_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            with open('events.json') as f:
                json_open = json.load(f)
            
            response = ""
            i = 1
            for event_dict in json_open["commands"]:
                response += "\n {}. ".format(str(i)) + event_dict['input']
                i += 1
            embed_var = discord.Embed(name="Alfredo Responses",
                                      colour=400597,
                                      type='rich')
            embed_var.set_author(name='Alfredo Bot',
                                 url="https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=LucasLucas",
                                 icon_url='https://static.scientificamerican.com/sciam/cache/file/ACF0A7DC-14E3-4263-93F438F6DA8CE98A_source.jpg?w=590&h=800&896FA922-DF63-4289-86E2E0A5A8D76BE1')
            embed_var.add_field(name="This is what I respond to: ", value=response)
            await ctx.channel.send(embed=embed_var)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        pass
    
def setup(client):
    client.add_cog(Command(client))
