import discord
from discord import app_commands
from discord.ext import commands
import sqlite3
import math
import random


class LevelSys(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Leveling is online!")

    @commands.Cog.listener()
    async def on_message(self,message:discord.Message):
        if message.author.bot:
            return
        connection = sqlite3.connect("./cogs./levels.db")
        cursor = connection.cursor()
        guild_id = message.guild.id
        user_id = message.author.id

        cursor.execute("SELECT * FROM Users WHERE guild_id = ? AND user_id = ?", (guild_id, user_id))
        result = cursor.fetchone()

        if result is None:
            cur_level = 0
            xp = 0
            level_up_xp = 100
            cursor.execute("INSERT INTO Users (guild_id, user_id, level, xp, level_up_xp) Values (?,?,?,?,?)", (guild_id,user_id,cur_level,xp,level_up_xp))

        else:
            cur_level = result[2]
            xp = result[3]
            level_up_xp = result[4]

            xp += random.randint(1,25)

        if xp >=level_up_xp:
            cur_level +=1
            new_level_up_xp = math.ceil(50 * cur_level ** 2 + 100 * cur_level + 50)
            await message.channel.send(f"{message.author.mention} has leveled up to the level {cur_level}")

            cursor.execute("UPDATE Users SET level = ? , xp = ? , level_up_xp =? WHERE guild_id = ? AND user_id =?", (cur_level,xp,new_level_up_xp,guild_id,user_id))
        
        cursor.execute("UPDATE Users SET xp = ? WHERE guild_id = ? AND user_id = ?", (xp,guild_id,user_id))
        connection.commit()
        connection.close()

    @app_commands.command(name="level",description="It will send you info of your level card")
    async def level(self,interation:discord.Interaction,member:discord.Member=None):
        if member is None:
            member = interation.user

        member_id=member.id
        guild_id=interation.guild.id
        connection = sqlite3.connect("./cogs/levels.db")
        cursor =connection.cursor()
        cursor.execute("SELECT * FROM Users WHERE guild_id =? AND user_id =?", (guild_id, member_id))
        result = cursor.fetchone()

        if result is None:
            await interation.response.send_message(f"{member.name} currently does not have a level .")
        else:
            level = result[2]
            xp = result[3]
            level_up_xp = result[4]

            # Create an embed message for the level card
            embed = discord.Embed(
                title=f"Level Card for {member.name}",
                color=discord.Color.blue()
            )
            embed.add_field(name="Level", value=str(level), inline=False)
            embed.add_field(name="XP", value=f"{xp} / {level_up_xp}", inline=False)
            embed.add_field(name="XP to Next Level", value=str(level_up_xp - xp), inline=False)
            embed.set_thumbnail(url=member.avatar.url)  # Display the user's avatar

            await interation.response.send_message(embed=embed)

        connection.close()

    @app_commands.command(name="leaderboard", description="Shows the server's top members based on level")
    async def leaderboard(self, interation: discord.Interaction):
        guild_id = interation.guild.id
        connection = sqlite3.connect("./cogs/levels.db")
        cursor = connection.cursor()

        # Fetch top 10 users by level and XP for the specified guild
        cursor.execute("""
        SELECT user_id, level, xp FROM Users
        WHERE guild_id = ?
        ORDER BY level DESC, xp DESC
        LIMIT 10
        """, (guild_id,))
        
        top_users = cursor.fetchall()
        connection.close()

        if not top_users:
            await interation.response.send_message("No leaderboard data available.")
            return

        # Create an embed for the leaderboard
        embed = discord.Embed(
            title=f"Leaderboard for {interation.guild.name}",
            color=discord.Color.gold()
        )

        # Format the top users in the embed
        for rank, (user_id, level, xp) in enumerate(top_users, start=1):
            user = interation.guild.get_member(user_id) or await self.bot.fetch_user(user_id)
            embed.add_field(
                name=f"{rank}. {user.name if user else 'Unknown User'}",
                value=f"Level: {level} | XP: {xp}",
                inline=False
            )

        await interation.response.send_message(embed=embed)

        connection.close()


async def setup(bot):
    await bot.add_cog(LevelSys(bot))