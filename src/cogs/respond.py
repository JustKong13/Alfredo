import json
import discord 
from discord.ext import commands
import random

class Event(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.embed = discord.Embed(colour=400597, type='rich')
        self.events = 'events.json'

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author == self.client.user:
            return

        with open('events.json') as f:    
            d = json.load(f)

        if '$' not in ctx.content:
            if ctx.author == self.client.user:
                return

            for event_obj in d["commands"]:
                if "$list_command" in ctx.content.lower():
                    break
                elif ctx.content.lower() == event_obj["input"].lower() or ctx.content.lower().startswith(event_obj["input"].lower() + " ") or ctx.content.lower().endswith(" " + event_obj["input"].lower()) or (" " + event_obj["input"].lower() + " " in ctx.content.lower()):
                    send = random.choice(event_obj["output"])
                    if '{}' in send:
                        embed_var = discord.Embed(colour=400597,
                                                    type='rich')
                        embed_var.add_field(name='Alfredo Bot', value=send.format(f'{ctx.author.mention}'), inline=False)
                        await ctx.channel.send(embed=embed_var)
                    elif '.com' in send:
                        await ctx.channel.send(send)
                    else:
                        embed_var = discord.Embed(colour=400597,
                                                    type='rich')
                        embed_var.add_field(name='Alfredo Bot', value=send, inline=False)
                        await ctx.channel.send(embed=embed_var)
                else:
                    pass
            
        for word in d["language"]:
            if word.lower() in ctx.content.lower() and (".net" not in ctx.content.lower() or ".com" not in ctx.content.lower()):
                self.embed.clear_fields()
                self.embed.add_field(name="Alfredo Bot", value="Watch your language", inline=False)
                await ctx.channel.send(embed=self.embed)
            
                user_missing = True # becomes false when user is found in file
                for tally_dict in d["tally"]:
                    #tally_dict = {
                    #    "user": {:obj:str}: user ID,
                    #    "tally": {obj:int}: number of times sworn
                    #}
                    
                    if f'{ctx.author.id}' == tally_dict["user"]:
                        user_missing = False
                        tally_dict['tally'] += 1
                    else:
                        pass
                    
                if user_missing:
                    d["tally"].append(
                        {
                            "user": f'{ctx.author.id}',
                            "tally": 1
                        }
                    )
                
                with open(self.events, 'w+') as update_file:
                    json.dump(d, update_file) 
        

        if ctx.author.id == 275738560902987777 and 'dick' in ctx.content.lower():
            await ctx.channel.send("People think that Bae Suzy overshadows the rest of the members of Miss A and they hate how everything is all about Suzy. This is one reason i come across alot. And just don't understand it. Okay yes she is super popular. She gets alot of Cfs, solo activities, dramas etc etc. But I don't see why it's her fault that she gets chosen for all of it. Plus more work demands more hardwork. She is a really hardworking girl and that's really admirable. For once people need to stop talking about the rest of the members of miss A while talking about Suzy and take her as an individual. She was really young when she got to be an idol and she had to work really hard to get to the top. Seriously guys its not just her face that is giving her the popularity bt her hardwork and attitude too. Disliking her for her popularity does not seem the right reason to me. :broken_heart:")
        
        if ctx.content.startswith("$"):
            message = str(ctx.content.split()[0])         
            if message[1:].isdigit():
                pass
            else:
                await ctx.channel.send("That command doesn't appear to exist. Use $help for help.")
                

def setup(client):
    client.add_cog(Event(client))
