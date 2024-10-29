import discord   
from discord.ext import commands , tasks
import os
import asyncio
from itertools import cycle
import logging
from dotenv import load_dotenv

load_dotenv(".env")
TOKEN: str = os.getenv("TOKEN")

logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

bot_status = cycle([f"type in '!help' for help", "thejuggler35","iloveyou", "love you too 😘","Arjun the great"])

@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(bot_status)))
@bot.event
async def on_ready():
    print("Bot ready !")
    change_status.start()
    try:
        synced_commands = await bot.tree.sync()
        print(f"Synced {len(synced_commands)} commands.")
    except Exception as e:
        print("An error with syncing application commands has occured : ", e)

@bot.tree.command(name="test" , description="testing first slash cmd .")
async def hello(interaction:discord.Interaction):
    await interaction.response.send_message(f"{interaction.user.mention} testing successfully you got it tj35")

@bot.tree.command(name="test2" , description="testing second (private) slash cmd .")
async def hello(interaction:discord.Interaction):
    await interaction.response.send_message(f"{interaction.user.mention} testing successfully you got it tj35",ephemeral=True)

async def Load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await Load()
        await bot.start(TOKEN)

asyncio.run(main())

