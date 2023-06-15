import discord, pymongo, random, json
from discord.ext import commands
from pymongo import MongoClient
from easy_pil import *

with open("./local data/level_exp.json", "r") as f:
    level_exp = json.load(f)

class Levels(commands.Cog):
    "Levelling"
    COG_EMOJI = "<a:Level_up:1118526299414220891>"

    def __init__(self, bot) -> None:
        self.bot = bot
        self.cluster = MongoClient("mongodb+srv://VegitoTy:59894179@cluster0.rlky3md.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.cluster["cookiechaos"]
        self.levels = self.db["Levels"]
    
    @commands.Cog.listener("on_message")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def levelmessages(self, message:discord.Message):
        if message.author.bot:
            return
        author = message.author; user_id = author.id
        guild = message.guild; guild_id = guild.id

        useri = self.levels.find_one({"_id":user_id, "guild_id":guild_id})
        if useri == None:
            self.levels.insert_one({"_id":user_id, "guild_id":guild_id, "level":0, "exp":0})
            useri = self.levels.find_one({"_id":user_id, "guild_id":guild_id})

        # xp needed for level up: 5 * (lvl ^ 2) + (50 * lvl) + 100
        # total xp needed for level: total xp of previous level + required xp of previous level

        add = random.randint(5, 15)
        new_exp = useri["exp"] + add

        userlevel = useri["level"]
        level_totalexp = level_exp.get(str(userlevel+1))

        if new_exp >= level_totalexp:
            userlevel+=1
            await message.channel.send(f"<a:Level_up:1118526299414220891> {message.author.mention} You just leveled up to level {userlevel}!")
        
        self.levels.replace_one(useri, {"_id":user_id, "guild_id":guild_id, "level":userlevel, "exp":new_exp})

    @commands.command(name='Rank', aliases=['rank'], description=f"Shows Someone's Level\nUsage:- cc,rank [user]")
    async def _rank(self, ctx:commands.Context, user:discord.Member=None):
        if user == None:
            user = ctx.author
        
        user_id = user.id
        guild_id = user.guild.id

        useri = self.levels.find_one({"_id":user_id, "guild_id":guild_id})
        if useri == None:
            return await ctx.send("<:Cross:1118556008227283085> You aren't ranked yet. Send some messages first, then try again.")

        level = useri["level"]
        exp = useri["exp"]
        totalexplvlup = level_exp.get(str(level+1))
        expcurrentlevel = totalexplvlup - exp
        expneededlvlup = 5 * (level ^ 2) + (50 * level) + 100
        percentage = round((exp/totalexplvlup)*100)

        background = Editor(Canvas((900,300), color="#141414"))
        profile_picture = await load_image_async(str(user.avatar.url))
        profile = Editor(profile_picture).resize((150,150)).circle_image()
        poppins = Font.poppins(size=40)
        poppins_small = Font.poppins(size=30)

        card_right_shape = [(600, 0), (750, 300), (900, 300), (900, 0)]

        background.polygon(card_right_shape, color="#FFFFFF")
        background.paste(profile, (30, 30))

        background.rectangle((30, 220), width=650, height=40, color="#FFFFFF")
        background.bar((30, 220), max_width=650, height=40, percentage=percentage, color="#FFFFFF", radius=20)

        background.text((200, 40), user.name, font=poppins, color="#FFFFFF")

        background.rectangle((200, 100), width=350, height=2, color="#FFFFFF")
        background.text((200, 130), f"Level: {level} | XP: {expcurrentlevel}", font=poppins_small, color="#FFFFFF")

        file = discord.File(fp=background.image_bytes, filename="levelcard.png")
        await ctx.send(file=file)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Levels(bot))