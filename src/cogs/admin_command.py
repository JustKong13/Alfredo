import discord 
from discord.ext import commands
import json


class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command()
    @commands.has_guild_permissions(manage_messages=True)
    async def purge(self, ctx, n):
        n = int(n)
        if n < 100:
            await ctx.channel.purge(limit=n+1)
        elif n > 100: 
            await ctx.channel.send("You are trying to purge too many message at once. Please choose a number less than 100.")

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            await ctx.send("Please make sure your command follows this format: $purge <number>")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please specify a number of messages you wish to delete')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to use this command. If you believe this is an error, please contact a moderator.")

    @commands.command()
    @commands.has_guild_permissions(manage_messages=True)
    async def add_command(self, ctx, *, text, help="Add a new command"):
        if ',' not in text:
            await ctx.channel.send("It seems as if you did not add an appropriate response. Please make sure to use this format: $add_command <input>, <output>")
        else:
            with open('events.json') as f:
                json_file = json.load(f)
            
            new_command = text.split(',', 1) # [input_str, output_str]
            if new_command[1].startswith(' '):
                new_command[1] = new_command[1][1:]
            found = False

            for command in json_file['commands']:
                if command['input'] == new_command[0]:
                    if new_command[1] in command['output']:
                        await ctx.channel.send('This command already exist!')
                    else:
                        command['output'].append(new_command[1])
                    found = True
                
            if found == False:
                d = {
                    "input": new_command[0],
                    "output": [new_command[1]]
                }
                json_file['commands'].append(d)
            
            with open('events.json', 'w') as update_file:
                json.dump(json_file, update_file)
                await ctx.channel.send("Your command has successfully been added.")

    @commands.command()
    @commands.has_guild_permissions(manage_messages=True)
    async def delete_command(self, ctx, *, text, help="To delete an Alfredo response"):
        pass


def setup(client):
    client.add_cog(Admin(client))