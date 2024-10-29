import discord
from discord.ext import commands

class Test(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command()
    async def ping(self,ctx):
        ping_embed = discord.Embed(title="Ping" , description="Latency in ms" , color=discord.Color.dark_gray())
        ping_embed.add_field(name=f"{self.bot.user.name} 's Latancy (ms) : ", value=f"{round(self.bot.latency*1000)}ms . ", inline=False)
        ping_embed.set_footer(text=f"Requested by {ctx.author.name} .", icon_url=ctx.author.avatar)
        await ctx.send(embed=ping_embed)
    @commands.command()
    async def Help(self,ctx):
        embeded_help = discord.Embed(title="HELP",description="List of the availble commands", color=discord.Color.gold())
        embeded_help.set_thumbnail(url=self.bot.user.avatar)
        embeded_help.add_field(name="!hello" , value="It will the bot creator name :) " , inline=False)
        embeded_help.add_field(name="!hi" , value="It will greet you" , inline=False)
        embeded_help.add_field(name="!gm , !goodmorning , !morning" , value="It will send you goodmorning msg" , inline=False)
        embeded_help.add_field(name="!ge , !goodevening , !evening" , value="It will send you good evening msg" , inline=False)
        embeded_help.add_field(name="!gn , !goodnight , !night" , value="It will send you goodnight msg" , inline=False)
        embeded_help.add_field(name="!botav" , value="It will show you bot avatar as well as give you link of it" , inline=False)
        embeded_help.add_field(name="!useravt" , value="It will show you user avatar as well as give you link of it" , inline=False)
        embeded_help.add_field(name="!ping" , value="It will show latancy in ms of the bot" , inline=False)
        embeded_help.set_image(url=ctx.guild.icon)
        embeded_help.set_footer(text=f"{ctx.author} need help" , icon_url=ctx.author.avatar)
        await ctx.send(embed=embeded_help)

    @commands.command()
    async def botav(self,ctx):
        # Replace ctx.author.avatar with bot.user.avatar
        url = self.bot.user.avatar.url  # Accessing the bot's avatar URL
        await ctx.send(f'Bot Avatar URL: {url}')

    @commands.command()
    async def userav(self,ctx):
        # Replace ctx.author.avatar with bot.user.avatar
        url = ctx.author.avatar.url  # Accessing the bot's avatar URL
        await ctx.send(f'User Avatar URL: {url}')

    @commands.command()
    async def hello(self,ctx):
        await ctx.send(f"Hello there , it's thejuggler35 , {ctx.author.mention}!")

    @commands.command(name="hi")
    async def greet(self,ctx):
        await ctx.send(f"Hello there , welcome to the server , {ctx.author.mention}!")

    @commands.command(aliases=["gm","morning"])
    async def goodmorning(self,ctx):
        await ctx.send(f"goodmorning , have a nice day :) {ctx.author.mention} ")

    @commands.command(aliases=["ge","evening"])
    async def goodevening(self,ctx):
        await ctx.send("goodevening , what to say idk :) ")

    @commands.command(aliases=["gn","night"])
    async def goodnight(self,ctx):
        await ctx.send(f"goodnight bro , aab soo bhi jao jaake {ctx.author.mention}")

    @commands.command()
    async def sendembed(self,ctx):
        embeded_msg = discord.Embed(title="Title of embed",description="Description of embed", color=discord.Color.green())
        embeded_msg.set_author(name="Header text" , icon_url=ctx.author.avatar)
        embeded_msg.set_thumbnail(url=ctx.author.avatar)
        embeded_msg.add_field(name="Name of field" , value="Value of field" , inline=False)
        embeded_msg.set_image(url=ctx.guild.icon)
        embeded_msg.set_footer(text="Footer text" , icon_url=ctx.author.avatar)
        await ctx.send(embed=embeded_msg)


async def setup(bot):
    await bot.add_cog(Test(bot))