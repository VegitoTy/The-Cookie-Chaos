import discord
from discord.ext import commands

error_emote = "❌"

class ErrorDetails(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)

    async def interaction_check(self, interaction: discord.Interaction):
        bot = getattr(interaction, "client", interaction._state._get_client())

        if (await bot.is_owner(interaction.user)):
            return True

        await interaction.response.send_message("Owner Only", ephemeral=True)
        
        return False
    
    @discord.ui.button(label="Details", custom_id="error_details", style=discord.ButtonStyle.red)
    async def _details(self, interaction:discord.Interaction, button:discord.ui.Button):
        exception = exception1
        self.interaction = interaction
        await interaction.response.send_message(exception)

class ErrorHandler(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot
    
    @commands.Cog.listener('on_command_error')
    async def errorhandler(self, ctx:commands.Context, exception):
        sus = False
        
        global exception1
        exception1 =  exception.__cause__ or exception

        view = ErrorDetails()

        if isinstance(exception1, commands.NotOwner):
            description = "> You are not the owner of this bot."
        elif isinstance(exception1, commands.CommandInvokeError):
            description = f"> Something went wrong during invocation of command `{ctx.command}`."
            sus = True
        elif isinstance(exception1, commands.CommandOnCooldown):
            description = f"> This command is on cooldown. Retry in `{exception1.retry_after:.2f}` seconds."
        elif isinstance(exception1, commands.errors.CheckFailure):
            description = "> You do not have the right permissions to use this command"
        elif isinstance(exception1, commands.errors.MissingRequiredArgument):
            args = ""
            for arg in exception1.args:
                args = args + f"`{arg[:-40]}`, "
            args = args[:-2]
            description = f"> Missing required argument(s): {args}"
        elif isinstance(exception1, commands.MemberNotFound):
            description = "> Member Not Found"
        elif isinstance(exception1, commands.UserNotFound):
            description = "> User Not Found"
        elif isinstance(exception1, commands.CommandNotFound):
            return None
        else:
            description = f"!! There was a error with this command\n{exception1}"
            sus = True

        embed = discord.Embed(title=f"{error_emote} Error", description=description, color=0x3498db)

        try:
            await ctx.reply(embed=embed, view=view)
        except exception1 as e:
            await ctx.send(embed=embed, view=view)
      
        if sus != False:
            raise exception1
            
async def setup(bot:commands.Bot) -> None:
    await bot.add_cog(
        ErrorHandler(bot)
    )