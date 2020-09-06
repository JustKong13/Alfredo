import discord 
from discord.ext import commands
import json


class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.events = 'events.json'


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
            with open(self.events) as f:
                json_file = json.load(f)
            
            new_command = text.split(',', 1) # [input_str, output_str]
            if new_command[1].startswith(' '):
                new_command[1] = new_command[1].strip()
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
            
            with open(self.events, 'w') as update_file:
                json.dump(json_file, update_file)
                await ctx.channel.send("Your command has successfully been added.")


    @commands.command()
    @commands.has_guild_permissions(manage_messages=True)
    async def remove_command(self, ctx, *, text, help="To delete an Alfredo response, please use this format: $remove_command <input>, <output>. Not providing an output will delete all responses to the input."):
        text_list = text.split(',', 1)
         
        with open(self.events) as f:
            json_file = json.load(f)

        for event_dict in json_file["commands"]:
            found = False

            # checks if the command is in the guild's database, and no output was specified to be deleted
            if text_list[0] == event_dict['input'] and len(text_list) == 1:
                found = True

                await ctx.channel.send("You are about to delete Alfredo's responses to {}. Type 'YES' to complete this action. Otherwise, please wait a moment.".format(text_list[0]))
                
                def check(message):
                    if message.author == ctx.author and message.content == "YES":
                        return True 
                
                await self.client.wait_for('message', timeout=10.0, check=check)

                # final conformation message
                del_responses = ''
                for response in event_dict['output']:
                    del_responses += "\n- " + response
                await ctx.channel.send("Alfredo's responses to {0} have been deleted. These are the deleted responses: {1}".format(text_list[0], del_responses))

                # update file
                json_file["commands"].remove(event_dict)
                with open(self.events, 'w') as update_file:
                    json.dump(json_file, update_file)


            # removes only the specified responce
            elif text_list[0] == event_dict['input'] and text_list[1].strip() in event_dict['output']:
                found = True

                await ctx.channel.send("You are about to delete the {0} response to {1}. Type 'YES' to complete this action. Otherwise, please wait a moment.".format(text_list[1].strip(), text_list[0]))

                def check(message):
                    if message.author == ctx.author and message.content == "YES":
                        return True

                await self.client.wait_for('message', timeout=10.0, check=check)
                await ctx.channel.send("Alfredo's response to {0} have been deleted. This is the deleted response: {1}".format(text_list[0], text_list[1].strip()))
                
                # removal of response
                event_dict["output"].remove(text_list[1].strip())
                with open(self.events, 'w') as update_file:
                    json.dump(json_file, update_file)

            elif text_list[0] == event_dict['input'] and text_list[1].strip() not in event_dict['output']:
                found = True
                response_str = ''
                for response in event_dict['output']:
                    response_str += "\n- "+ response
                await ctx.channel.send("Sorry your specific response was not found. Here are the available responses to {0}: {1}".format(text_list[0], response_str))
                

        if found == False:
            await ctx.channel.send("Sorry your input was not found. Use $list_command to see a list of key words Alfredo responds to!")


    @remove_command.error
    async def remove_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.channel.send("No input was specified. Please use $list_command to see a list of terms to remove.")
        else:
            await ctx.channel.send("Your request was not completed. Please use $remove_command again if this was a mistake.")
            



def setup(client):
    client.add_cog(Admin(client))
