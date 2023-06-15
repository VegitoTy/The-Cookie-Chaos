import discord, os
from discord.ext import commands

with open("./secret") as e:
    TOKEN = e.read().strip()

class CookieChaos(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or("cc,"),
            status=discord.Status.idle,
            activity=discord.Activity(type=discord.ActivityType.watching, name="The Cookie Chaos"),
            intents=discord.Intents.all()
        )
    
    async def setup_hook(self):
        for filename in os.listdir('./bot/extensions'):
            if filename.endswith('.py'):
                extension = f"bot.extensions.{filename[:-3]}"
                await self.load_extension(extension)
        await self.load_extension('bot.help.cog')
        await self.load_extension('jishaku')
        await bot.tree.sync()

    async def on_ready(self):
        channel = await self.fetch_channel(1118514881268826132)
        await channel.send("Bot Has Started.")
        print(f'Logged In As {self.user}')
    
    async def close(self):
        channel = await self.fetch_channel(1118514881268826132)
        await channel.send("Bot Has Stopped.")
        print(f'Logging Out..')
        await super().close()

    async def is_owner(self, user:discord.User):
        if user.id == 766508994390523926:
            return True

        return await super().is_owner(user)

if __name__ == '__main__':
    bot = CookieChaos()
    bot.run(TOKEN)