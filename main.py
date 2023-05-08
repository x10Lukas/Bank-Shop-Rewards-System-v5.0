import discord
from discord.ext import commands

pre = "!"
token = "<YOUR DISCORD BOT TOKEN>"

bot = commands.Bot(command_prefix=f"{pre}", case_intensive=True, intents=discord.Intents.all())
bot.remove_command('help')
bot.launch_time = datetime.utcnow()

@bot.event
async def on_ready():
    print(f'{bot.user.name}')
    print(f'{bot.user.id}')
    print("Online")
    print("-------------")
    await bot.load_extension("cogs.bank")
    
bot.run(token)
