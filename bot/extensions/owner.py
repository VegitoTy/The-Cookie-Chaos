import discord, ast
from discord.ext import commands

class Owner(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @commands.command(name='Eval', aliases=['eval', 'ev'], description="Owner Only So No Use Of Description lol.")
    @commands.is_owner()
    async def _eval(self, ctx:commands.Context, *, cmd):
        """Evaluates input.
Input is interpreted as newline seperated statements.
If the last statement is an expression, that is the return value.
Usable globals:
    - `bot`: the bot instance
    - `discord`: the discord module
    - `commands`: the discord.ext.commands module
    - `ctx`: the invokation context
    - `__import__`: the builtin `__import__` function
Such that `>eval 1 + 1` gives `2` as the result.
The following invokation will cause the bot to send the text '9'
to the channel of invokation and return '3' as the result of evaluating
>eval ```
a = 1 + 2
b = a * 2
await ctx.send(a + b)
a
```
"""

        def insert_returns(body):
            if isinstance(body[-1], ast.Expr):
                body[-1] = ast.Return(body[-1].value)
                ast.fix_missing_locations(body[-1])

            if isinstance(body[-1], ast.If):
                insert_returns(body[-1].body)
                insert_returns(body[-1].orelse)

            if isinstance(body[-1], ast.With):
                insert_returns(body[-1].body)

        fn_name = "_eval_expr"

        cmd = cmd.strip("` ")

        cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

        body = f"async def {fn_name}():\n{cmd}"

        parsed = ast.parse(body)
        body = parsed.body[0].body

        insert_returns(body)

        env = {
            'bot': ctx.bot,
            'guild': ctx.guild,
            'discord': discord,
            'commands': commands,
            'ctx': ctx,
            '__import__': __import__
        }
        exec(compile(parsed, filename="<ast>", mode="exec"), env)
    
        result = (await eval(f"{fn_name}()", env))
        await ctx.send(result)

async def setup(bot:commands.Bot) -> None:
    await bot.add_cog(
        Owner(bot)
    )