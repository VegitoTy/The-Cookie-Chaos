import discord
from discord.ext import commands

class Utility(commands.Cog):
    """Utility Commands"""
    COG_EMOJI = "🔧"

    def __init__(self, bot) -> None:
        self.bot = bot
    
    @commands.command(name='AV', aliases=['av'], description=f"Shows Someone's Avatar.\nUsage:- &Av [user]")
    async def avatar(self, ctx:commands.Context, member:discord.Member=None):
        """Shows Someone's Avatar."""
        if member == None:
            member = ctx.message.author
        
        embed = discord.Embed(color=0x3498db, title=f"{member}'s avatar")
        try:
            embed.set_image(url=member.display_avatar.url)
        except AttributeError:
            embed.set_image(url=member.default_avatar.url)
        await ctx.reply(embed=embed)

    @commands.command(aliases=['embed'], name='Embed', description=f"Creates A Embed Separate The Title From The Description With |\nUsage:- &Embed Title|Description")
    @commands.check_any(commands.has_permissions(administrator=True), commands.is_owner())
    async def _embed(self, ctx:commands.Context, channel:discord.TextChannel, *, text:str):
        """Creates A Embed Separate The Title From The Description With |"""
        try:
            title, description = text.split("|", 1)
            embed = discord.Embed(title=title, description=description, color=0x3498db)
            await channel.send(embed=embed)
            await ctx.message.add_reaction("✅")
        except Exception as e:
            await ctx.message.add_reaction("❌")
            raise e
    
    @commands.command(name='Echo', aliases=['echo'], description=f"Make The Bot Send A Message\nUsage:- &Echo [message]")
    @commands.is_owner()
    async def _echo(self, ctx:commands.Context, *, message:str):
        """Make The Bot Send A Message"""
        await ctx.message.delete()
        await ctx.send(message)
    
    @commands.command(name='Userinfo', aliases=['whois', 'ui', 'UI'], description=f"Shows The Info Of A User\nUsage:- &Ui [User]")
    async def _ui(self, ctx:commands.Context, user:discord.User=None):
        """Shows The Info Of A User"""
        if not user:
            user = ctx.author
        
        member = await ctx.guild.query_members(user_ids=[user.id])
        if len(member) == 0:
            created_at = user.created_at
            embed = discord.Embed(colour=0x3498db, timestamp=ctx.message.created_at)
            embed.set_author(name=f'User Info - {user}')
            embed.set_thumbnail(url=user.avatar.url)
            embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.display_avatar.url)
            embed.add_field(name='ID: ', value=user.id, inline=False)
            embed.add_field(name='Name: ',value=user.name,inline=False)
            embed.add_field(name='Created at:',value=discord.utils.format_dt(dt=created_at),inline=False)
        else:
            member:discord.Member = member[0]
            created_at = member.created_at
            joined_at = member.joined_at
            rlist = []
            ignored_roles = 0
            for role in member.roles:
                if len(rlist) >= 15:
                    ignored_roles += 1
                if role.name != "@everyone" and len(rlist) < 15:
                    rlist.append(role.mention)
            e = ""
            for role in rlist:
                e += f"{role}, "     
            embed = discord.Embed(colour=member.color, timestamp=ctx.message.created_at)
            embed.set_author(name=f'User Info - {member}')
            embed.set_thumbnail(url=member.avatar.url)
            embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.display_avatar.url)
            embed.add_field(name='ID: ',value=member.id,inline=False)
            embed.add_field(name='Name:',value=member.name,inline=False)
            embed.add_field(name='Created at:',value=discord.utils.format_dt(created_at),inline=False)
            embed.add_field(name='Joined at:',value=discord.utils.format_dt(joined_at),inline=False)
            if ignored_roles == 0:
                embed.add_field(name=f'Roles: {len(member.roles)}', value=f'{e[:-2]}',inline=False)
            else:
                embed.add_field(name=f'Roles: {len(member.roles)}', value=f'{e[:-2]} And {ignored_roles} more roles..',inline=False)
            embed.add_field(name='Top Role:',value=member.top_role.mention,inline=False)
        await ctx.send(f'Info about {user}', embed=embed)

async def setup(bot:commands.Bot):
    await bot.add_cog(
        Utility(bot)
    )