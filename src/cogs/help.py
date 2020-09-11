import discord
from discord.ext import commands


class Help(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx, command=None):
        embed_var = discord.Embed(colour=400597, type='rich')
        embed_var.set_author(name="Alfredo Bot Help Menu", 
                             url="https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=LucasLucas",
                             icon_url='https://lh3.googleusercontent.com/3cSB32pX5QEEvG6yLLBPyDLOx6814WwGqrOlg8I4PkXeMZcdFrZhb28LGtYRgS_WHqps=s136')
        embed_var.set_footer(text="Click Alfredo Bot Help Menu for a surprise!")
        if command == None:
            embed_var.set_footer(text="Use $help admin for admin commands")
            embed_var.add_field(name="8ball", value="Ask me a question!\n$8ball <question>", inline=True)
            embed_var.add_field(name="Roll", value="Roll a random number\n$roll <minimum> <maximum>", inline=True)
            embed_var.add_field(name="List", value="List out Alfredo's key words or responses\n$list <key word>", inline=True)
            embed_var.add_field(name="Test", value="Checks latency of Alfredo bot", inline=True)
            embed_var.add_field(name="opgg", value="Check out a player's opgg page\n$opgg <player IGN>", inline=True)
            embed_var.add_field(name="Alarm", value="Command coming soon", inline=True)
            embed_var.add_field(name="Stopwatch", value="Command coming soon", inline=True)
            embed_var.add_field(name="Timer", value="Command coming soon", inline=True)
            embed_var.add_field(name="play", value="Command coming soon\nPlays a Spotify Playlist", inline=True)

        elif command.lower() == 'admin':
            embed_var.add_field(name='Purge', value="Deletes a number of previous messages\n$purge <number>", inline=True)
            embed_var.add_field(name="add_command", value="Adds a response to a key word/phrase\n$add_command <key word/phrase>, <response>")
            embed_var.add_field(name="remove_command", value="Removes either a response.\nNOTE: Not specifying a response deletes all responses\n$remove_command <key word>, <response>")
        await ctx.channel.send(embed=embed_var)

def setup(client):
    client.add_cog(Help(client))
