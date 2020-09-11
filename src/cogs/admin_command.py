import discord 
from discord.ext import commands
import json


class Admin(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.events = 'events.json'
        self.icon_url = "https://lh3.googleusercontent.com/3cSB32pX5QEEvG6yLLBPyDLOx6814WwGqrOlg8I4PkXeMZcdFrZhb28LGtYRgS_WHqps=s136"
        self.author = "Alfredo Bot"



    @commands.command()
    @commands.has_guild_permissions(manage_messages=True)
    async def purge(self, ctx, n):
        n = int(n)
        if n < 100:
            await ctx.channel.purge(limit=n+1)
        elif n >= 100: 
            embed_var = discord.Embed(colour=400597, type='rich')
            embed_var.set_author(name=self.author, 
                                icon_url=self.icon_url)
            embed_var.add_field(name='ERROR', value="You are trying to purge too many commands at once. Please choose a number less than 100.")
            await ctx.channel.send(embed=embed_var)

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            embed_var = discord.Embed(colour=400597, type='rich')
            embed_var.set_author(name=self.author, 
                                icon_url=self.icon_url)
            embed_var.add_field(name='ERROR', value="Please make sure your command follows this format: $purge <number>")
            await ctx.channel.send(embed=embed_var)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed_var = discord.Embed(colour=400597, type='rich')
            embed_var.set_author(name=self.author, 
                                icon_url=self.icon_url)
            embed_var.add_field(name='ERROR', value="Please specify a number of messages you wish to delete")
            await ctx.channel.send(embed=embed_var)
        elif isinstance(error, commands.MissingPermissions):
            embed_var = discord.Embed(colour=400597, type='rich')
            embed_var.set_author(name=self.author, 
                                icon_url=self.icon_url)
            embed_var.add_field(name='ERROR', value="You do not have permission to use this command. If you believe this is an error, please contact a moderator")
            await ctx.channel.send(embed=embed_var)


    @commands.command()
    @commands.has_guild_permissions(manage_messages=True)
    async def add_command(self, ctx, *, text, help="Add a new command"):
        if ',' not in text:
            embed_var = discord.Embed(colour=400597, type='rich')
            embed_var.set_author(name=self.author, 
                                 icon_url=self.icon_url)
            embed_var.add_field(name='ERROR', value="It seems as if you did not add an appropriate response. Please make sure to use this format: $add_command <input>, <output>")
            await ctx.channel.send(embed=embed_var)
        else:
            with open(self.events) as f:
                json_file = json.load(f)
            
            new_command = text.split(',', 1) # [input_str, output_str]
            if new_command[1].startswith(' '):
                new_command[1] = new_command[1].strip()
            found = False

            for event_dict in json_file['commands']:
                if event_dict['input'] == new_command[0] and new_command[1] in event_dict['output']:
                    embed_var = discord.Embed(colour=400597, type='rich')
                    embed_var.set_author(name=self.author, 
                                        icon_url=self.icon_url)
                    embed_var.add_field(name='ERROR', value="This command already exist!")
                    await ctx.channel.send(embed=embed_var)
                    found = True
                elif event_dict['input'] == new_command[0] and new_command[1] not in event_dict['output']:
                    event_dict['output'].append(new_command[1])
                    embed_var = discord.Embed(colour=400597, type='rich')
                    embed_var.set_author(name=self.author, 
                                        icon_url=self.icon_url)
                    embed_var.add_field(name='Command added!', value="Your command has been successfully added")
                    await ctx.channel.send(embed=embed_var)
                    found = True
                
            if found == False:
                d = {
                    "input": new_command[0],
                    "output": [new_command[1]]
                }
                json_file['commands'].append(d)
                embed_var = discord.Embed(colour=400597, type='rich')
                embed_var.set_author(name=self.author, 
                                    icon_url=self.icon_url)
                embed_var.add_field(name='Command added!', value="Your command has been successfully added")
                await ctx.channel.send(embed=embed_var)
            
            with open(self.events, 'w') as update_file:
                json.dump(json_file, update_file)
            


    @commands.command(help="To delete an Alfredo response, please use this format: $remove_command <input>, <output>. Not providing an output will delete all responses to the input.")
    @commands.has_guild_permissions(manage_messages=True)
    async def remove_command(self, ctx, *, text):
        text_list = text.split(',', 1)
         
        with open(self.events) as f:
            json_file = json.load(f)

        for event_dict in json_file["commands"]:

            # checks if the command is in the guild's database, and no output was specified to be deleted
            if text_list[0] == event_dict['input'] and len(text_list) == 1:
                found = True

                embed_var = discord.Embed(colour=400597, type='rich')
                embed_var.set_author(name=self.author, 
                                    icon_url=self.icon_url)
                embed_var.add_field(name='CONFIRM', value="You are about to remove all responses to {}. Please confirm by typing 'YES'".format(text_list[0].split()))
                await ctx.channel.send(embed=embed_var)
                
                def check(message):
                    if message.author == ctx.author and message.content == "YES":
                        return True 
                
                await self.client.wait_for('message', timeout=10.0, check=check)

                # final conformation message
                del_responses = ''
                for response in event_dict['output']:
                    del_responses += "\n- " + response
                embed_var = discord.Embed(colour=400597, type='rich')
                embed_var.set_author(name=self.author, 
                                    icon_url=self.icon_url)
                embed_var.add_field(name='ERROR', value="Alfredo's responses to '{0}' have been deleted. These are the deleted responses: {1}".format(text_list[0].strip(), del_responses))
                await ctx.channel.send(embed=embed_var)

                # update file
                json_file["commands"].remove(event_dict)
                with open(self.events, 'w') as update_file:
                    json.dump(json_file, update_file)


            # removes only the specified responce
            elif text_list[0] == event_dict['input'] and text_list[1].strip() in event_dict['output']:
                found = True

                embed_var = discord.Embed(colour=400597, type='rich')
                embed_var.set_author(name=self.author, 
                                    icon_url=self.icon_url)
                embed_var.add_field(name='ERROR', value="You are about to delete the '{0}' response to '{1}'. Type 'YES' to complete this action. Otherwise, please wait a moment.".format(text_list[1].strip(), text_list[0]))
                await ctx.channel.send(embed=embed_var)

                def check(message):
                    if message.author == ctx.author and message.content == "YES":
                        return True

                await self.client.wait_for('message', timeout=10.0, check=check)

                embed_var = discord.Embed(colour=400597, type='rich')
                embed_var.set_author(name=self.author, 
                                    icon_url=self.icon_url)
                embed_var.add_field(name='Command deleted', value="All responses to '{}' have been deleted".format(text_list[0].strip()))
                await ctx.channel.send(embed=embed_var)
                
                # removal of response
                event_dict["output"].remove(text_list[1].strip())
                with open(self.events, 'w') as update_file:
                    json.dump(json_file, update_file)

            elif text_list[0] == event_dict['input'] and text_list[1].strip() not in event_dict['output']:
                found = True
                response_str = ''
                for response in event_dict['output']:
                    response_str += "\n- "+ response
                
                embed_var = discord.Embed(colour=400597, type='rich')
                embed_var.set_author(name=self.author, 
                                    icon_url=self.icon_url)
                embed_var.add_field(name='ERROR', value="Sorry your specific response was not found. Here are the available responses to '{0}': {1}".format(text_list[0], response_str))
                await ctx.channel.send(embed=embed_var)
            
            else:
                found = False
                

        if found == False:
            embed_var = discord.Embed(colour=400597, type='rich')
            embed_var.set_author(name=self.author, 
                                icon_url=self.icon_url)
            embed_var.add_field(name='ERROR', value="Sorry your input was not found. Use $list_command to see a list of key words Alfredo responds to!")
            await ctx.channel.send(embed=embed_var)

    @remove_command.error
    async def remove_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed_var = discord.Embed(colour=400597, type='rich')
            embed_var.set_author(name=self.author, 
                                icon_url=self.icon_url)
            embed_var.add_field(name='ERROR', value="No input was specified. Please use $list_command to see a list of terms to remove.")
            await ctx.channel.send(embed=embed_var)
        elif isinstance(error, commands.MissingPermissions):
            embed_var = discord.Embed(colour=400597, type='rich')
            embed_var.set_author(name=self.author, 
                                icon_url=self.icon_url)
            embed_var.add_field(name='ERROR', value="You do not have permission to use this command. If you believe this is an error, please contact a moderator")
            await ctx.channel.send(embed=embed_var)
        else:
            embed_var = discord.Embed(colour=400597, type='rich')
            embed_var.set_author(name=self.author, 
                                icon_url=self.icon_url)
            embed_var.add_field(name='ERROR', value="Your request was not completed")
            await ctx.channel.send(embed=embed_var)
            



def setup(client):
    client.add_cog(Admin(client))
