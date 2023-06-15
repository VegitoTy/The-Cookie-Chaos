import discord
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @commands.Cog.listener('on_member_join')
    async def welcome(self, member:discord.Member):
        channel = member.guild.get_channel(1117081282292236350)
        embed=discord.Embed(title=f"Welcome {member} to {member.guild}", description=f"Hello {member.mention}, you're the {member.guild.member_count} member here!", color=0xffffff)
        await channel.send(embed=embed)

async def setup(bot:commands.Bot) -> None:
    await bot.add_cog(
        Events(bot)
    )