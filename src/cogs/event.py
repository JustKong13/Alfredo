import json
import discord 
from discord.ext import commands
import random

class Event(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if "$" not in ctx.content:
            with open('events.json') as f:    
                d = json.load(f)

                if ctx.author == self.client.user:
                    return

                for event_obj in d["commands"]:
                    if "$list_command" in ctx.content.lower():
                        break
                    elif ctx.content.lower() == event_obj["input"].lower() or ctx.content.lower().startswith(event_obj["input"].lower() + " ") or ctx.content.lower().endswith(" " + event_obj["input"].lower()) or (" " + event_obj["input"].lower() + " " in ctx.content.lower()):
                        send = random.choice(event_obj["output"])
                        if '{}' in send:
                            await ctx.channel.send(send.format(f'{ctx.author.mention}'))
                        else:
                            await ctx.channel.send(send)
                    else:
                        pass


def setup(client):
    client.add_cog(Event(client))
