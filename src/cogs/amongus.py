import discord
from discord.ext import commands


class amongUs(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.icon_url = "https://lh3.googleusercontent.com/VHB9bVB8cTcnqwnu0nJqKYbiutRclnbGxTpwnayKB4vMxZj8pk1220Rg-6oQ68DwAkqO"
        self.author = "Alfredo Bot"
        self.embed = discord.Embed(colour=400597, type='rich')
        self.code = None

    @commands.command()
    @commands.has_guild_permissions(manage_messages=True)
    async def start_game(self, ctx, code):
        if len(code) == 6:
            self.code = code
            await ctx.channel.send("@everyone AMONG US CODE: **{}**".format(code.upper()))
        else:
            self.embed.clear_fields()
            self.embed.set_author(name=self.author, 
                                  icon_url=self.icon_url)
            self.embed.add_field(name="Invalid Code", value="This is not a valid code.", inline=False)
            await ctx.channel.send(embed=self.embed)

    @commands.command()
    @commands.has_guild_permissions(manage_messages=True)
    async def end_game(self, ctx):
        if self.code == None:
            self.embed.clear_fields()
            self.embed.set_author(name=self.author, 
                                  icon_url=self.icon_url)
            self.embed.add_field(name="ERROR", value="There is currently no ongoing game.", inline=False)
            await ctx.channel.send(embed=self.embed)
        else:
            self.embed.clear_fields()
            self.embed.set_author(name=self.author, 
                                  icon_url=self.icon_url)
            self.embed.add_field(name="Among Us", value="Thanks for playing!", inline=False)
            self.code = None
            await ctx.channel.send(embed=self.embed)

    @commands.command()
    @commands.has_guild_permissions()
    async def code(self, ctx):
        if self.code:
            await ctx.channel.send("Among Us code: **{}**".format(self.code.upper()))
        else:
            self.embed.clear_fields()
            self.embed.set_author(name=self.author, 
                                  icon_url=self.icon_url)
            self.embed.add_field(name="ERROR", value="There is currently no ongoing game.", inline=False)
            await ctx.channel.send(embed=self.embed)

def setup(client):
    client.add_cog(amongUs(client))