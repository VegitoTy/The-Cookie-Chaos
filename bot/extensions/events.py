import discord
from discord.ext import commands

class Events(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @commands.Cog.listener('on_member_join')
    async def _welcome(self, member:discord.Member):
        channel = await member.guild.fetch_channel(1117081282292236350)
        embed=discord.Embed(title=f"Welcome {member} to {member.guild}", description=f"Hello {member.mention}, you're the {member.guild.member_count} member here!", color=0x2c2d31)
        try:
            embed.set_thumbnail(url=member.avatar.url)
        except AttributeError:
            pass
        await channel.send(content=member.mention, embed=embed)

async def setup(bot:commands.Bot) -> None:
    await bot.add_cog(
        Events(bot)
    )