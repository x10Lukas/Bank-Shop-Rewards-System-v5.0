import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import asyncio
from asyncio import sleep
import random
import time
import json
import io
import os
import requests
import DiscordUtils
from discord import utils, app_commands
from math import *
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops, ImageOps
import pytz
from fortnite_api import Account
from discord import File
from easy_pil import Editor, load_image_async, Font
from typing import Optional
from discord import ui
from pstats import Stats
import scrapetube
import aiosqlite
import sqlite3
import hashlib
import string
from captcha.image import ImageCaptcha
import string
import twitchio
from reportlab.pdfgen import canvas

## Config ###
def get_config(name):
  with open("config.json", "r") as f:
    json_file = json.load(f)
    return json_file[name]

token = get_config("token") 
guild_id = get_config("guild_id") 
log_channel = get_config("log_channel")
pre = "!"
role_id = "850405532703784970"

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
    await bot.load_extension("cogs.chatgpt")
    await bot.load_extension("cogs.help")
    await bot.load_extension("cogs.level")
    await bot.load_extension("cogs.moderation")
    await bot.load_extension("cogs.ticket")
    await bot.tree.sync()
    bot.loop.create_task(status_task())
    bot.add_view(applymenu())
    bot.add_view(VerifyButtons())
    bot.add_view(SuggestionButtons("Question","Upvote", "Downvote"))
    bot.add_view(SuggestionModal())
    bot.add_view(FeedbackModal()) 
    bot.add_view(PartnerButtons())
    bot.add_view(PartnerModal())
    bot.add_view(GiveawayView())
    # bot.add_view(ReportModal(original_message=message))

async def status_task():
  while True:
    await bot.change_presence(activity=discord.Game(f'type {pre} for more...'), status=discord.Status.online)
    await asyncio.sleep(5)
    await bot.change_presence(activity=discord.Game('coded by Lukas21#9627'), status=discord.Status.online)
    await asyncio.sleep(5)

# #Welcome Event#
# @bot.event
# async def on_guild_join(guild):
#   bot_entry = await guild.audit_logs(action=discord.AuditLogAction.bot_add).flatten()
#   embed = discord.Embed(description="Hello! Thanks for inviting me!", color=int(get_config("colors")["embed_color"], 16))
#   embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon}")
#   embed.set_image(url=f"{guild.icon}")
#   embed.set_footer(text=f"{guild.guild.name}", icon_url=f"{guild.guild.icon}")
#   await bot_entry[0].user.send(embed=embed)

@bot.event
async def on_member_join(member: discord.Member):
  channel = bot.get_channel(765333287447035924)

  roleA = discord.utils.get(member.guild.roles, name="✌️・COMMUNITY・✌️")
  roleB = discord.utils.get(member.guild.roles, name="⠀⠀⠀⠀⠀⠀⠀⠀⠀About Me⠀⠀⠀⠀⠀⠀⠀⠀⠀")
  roleC = discord.utils.get(member.guild.roles, name="⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀Age⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
  roleD = discord.utils.get(member.guild.roles, name="⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀Gender⠀⠀⠀⠀⠀⠀  ⠀⠀   ⠀")
  roleE = discord.utils.get(member.guild.roles, name="⠀⠀⠀⠀⠀⠀ ⠀⠀⠀⠀Origin⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀")
  roleF = discord.utils.get(member.guild.roles, name="⠀⠀⠀⠀  ⠀ ⠀    ⠀⠀⠀⠀DM⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
  await member.add_roles(roleA)
  await member.add_roles(roleB)
  await member.add_roles(roleC)
  await member.add_roles(roleD)
  await member.add_roles(roleE)
  await member.add_roles(roleF)

  pos = sum(m.joined_at < member.joined_at for m in member.guild.members if m.joined_at is not None)

  if pos == 1:
    te = "str"
  elif pos == 2:
    te = "nd"
  elif pos == 3:
    te = "rd"
  else: pos == "th"      

  background = Editor("background.png")
  profile_image = await load_image_async(str(member.display_avatar))


  profile = Editor(profile_image).resize((160, 155)).circle_image()
  poppins = Font.poppins(size=25, variant="regular")

  poppins_small = Font.poppins(size=20, variant="light")

  background.paste(profile, (290, 40))
  background.ellipse((290, 40), 160, 155, outline="white", stroke_width=4)

  background.text((380, 250), f"{member} just joined the Server", color="white", font=poppins, align="center")
  background.text((380, 300), f"Member #{len(list(member.guild.members))}", color="white", font=poppins_small, align="center")

  file = File(fp=background.image_bytes, filename="background.png")
  embed = discord.Embed(title=f"Welcome to `{member.guild.name}`", description=f"Hey, {member.mention} | {member.name},\n Welcome to the **{member.guild.name}** Discord Server!", color=int(get_config("colors")["embed_color"], 16))
  embed.set_thumbnail(url=f"{member.display_avatar}")
  embed.set_image(url="attachment://background.png")
  await channel.send(embed=embed, file=file)

  guild = member.guild
  voice_channel = member.guild.get_channel(1075748286901800991)
  await voice_channel.edit(name=f"⚫┃・Members: {str(guild.member_count)}")

@bot.event
async def on_member_remove(member):  
    embed = discord.Embed(color=int(get_config("colors")["embed_color"], 16), title=f"Left the `{member.guild.name}`", description=f"Hey, {member.mention} | `{member}`, left the **{member.guild.name}** Discord Server!")
    embed.set_thumbnail(url=f"{member.display_avatar.url}")
    embed.set_footer(text=f"You are the {len(list(member.guild.members))} Member", icon_url=f"{member.guild.icon}")
    embed.timestamp = datetime.utcnow()
    channel = bot.get_channel(769114713048875008)
    await channel.send(embed=embed)

    guild = member.guild
    voice_channel = member.guild.get_channel(1075748286901800991)
    await voice_channel.edit(name=f"⚫┃・Members: {str(guild.member_count)}")

# @bot.event
# async def on_presence_update(before, after):
#   online_members = []
#   offline_members = []
#   for member in after.guild.members:
#       if member.status is not discord.Status.offline:
#           online_members.append(member.name)
#       else:
#           offline_members.append(member.name)

#   online_channel = after.guild.get_channel(1082760464573935656)
#   while True:
#     try:
#       await online_channel.edit(name=f"🟢┃・Online: {len(online_members)}")
#       break
#     except discord.errors.Forbidden:
#       print("I don't have permission to edit the channel name.")
#       break
#     except discord.errors.HTTPException as e:
#       if e.status == 900:
#         print(f"Got rate-limited, retrying in {e.retry_after} seconds.")
#         await asyncio.sleep(e.retry_after)
#       else:
#         raise

#   offline_channel = before.guild.get_channel(1082760552159391865)
#   while True:
#     try:
#       await offline_channel.edit(name=f"🔴┃・Offline: {len(offline_members)}")
#       break
#     except discord.errors.Forbidden:
#       print("I don't have permission to edit the channel name.")
#       break
#     except discord.errors.HTTPException as e:
#       if e.status == 900:
#         print(f"Got rate-limited, retrying in {e.retry_after} seconds.")
#         await asyncio.sleep(e.retry_after)
#       else:
#         raise

@bot.event
async def on_application_command_error(ctx, error):
  await ctx.respond(f"Es ist ein fehler aufgetreten: ```{error}```")
  raise error

@bot.tree.command()
@commands.has_permissions(administrator=True)
async def allrole(interaction: discord.Interaction):
    members = interaction.guild.members
    for member in members:
      try:
        roleA = interaction.guild.get_role(1072639693595889664)
        roleB = interaction.guild.get_role(1072640058450002020)
        roleC = interaction.guild.get_role(1072640790297329714)
        roleD = interaction.guild.get_role(1072641278711431230)
        roleE = interaction.guild.get_role(1072641199040626819)
        await member.add_roles(roleA)
        await member.add_roles(roleB)
        await member.add_roles(roleC)
        await member.add_roles(roleD)
        await member.add_roles(roleE)
        print("Add Role to: " + member.name)
      except:
        print("Couldn't add role to " + member.name)

@bot.command()
async def uptime(ctx):
    time2 = datetime.utcnow().strftime("%A, %B %d, %Y %H:%M")
    delta_uptime = datetime.utcnow() - bot.launch_time
    hours, remainder = (int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = (remainder, 60)
    days, hours = (hours, 24)

    embed = discord.Embed(title=f"✅ {ctx.guild.name} Uptime", description=f"``` {hours} Hrs︲{minutes} Mins︲{seconds} Secs ```\n**Date Launched**\n{time2}", color=int(get_config("colors")["embed_color"], 16))
    embed.set_thumbnail(url=f"{ctx.guild.icon}")
    embed.set_footer(text=f'{ctx.guild.name}', icon_url=f"{ctx.guild.icon}")
    await ctx.reply(embed=embed, mention_author=False)

@bot.command(aliases=['p'])
async def ping(ctx):
    embed = discord.Embed(description=f"`{round(bot.latency * 1000)} ms`", color=int(get_config("colors")["embed_color"], 16))
    embed.set_author(name=f"PING", icon_url="https://cdn.discordapp.com/emojis/798953395062702151.png?v=1")
    embed.set_footer(text=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
    await ctx.reply(embed=embed, mention_author=False)

@bot.command()
async def invites(ctx, member: discord.Member=None):
    if member == None: member = ctx.author
    total_invites = 0
    for i in await ctx.guild.invites():
        if i.inviter == member:
            total_invites += i.uses
    embed = discord.Embed(description=f"{member.mention} has invited `{total_invites}` member{'' if total_invites == 1 else 's'}!", color=int(get_config("colors")["embed_color"], 16))
    embed.set_author(name=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
    embed.set_footer(text=f"{ctx.guild.name}",icon_url=f"{ctx.guild.icon}")
    await ctx.reply(embed=embed, mention_author=False)      

@bot.event
async def on_invite_command(invite):
    invitechannel = bot.get_channel(850409719113842769) # Remember how to get channel IDs?
    embed = discord.Embed(title="New Invite",description=f"Created by {invite.inviter}\nCode: {str(invite)}")
    await invitechannel.send(embed=embed)

#Say Command#
@bot.command()
@commands.has_permissions(manage_messages=True)
async def say(ctx,*,message):
  embed=discord.Embed(description=f"{message}", color=int(get_config("colors")["embed_color"], 16))
  embed.set_author(name=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
  embed.set_footer(text=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
  message=await ctx.channel.send(embed=embed) 

@bot.command()
@commands.has_permissions(manage_messages=True)
async def partner(ctx,*,message):
  emb=discord.Embed(title="**How to Partner**", description=f"{message}", color=int(get_config("colors")["embed_color"], 16))
  emb.set_author(name=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
  emb.set_thumbnail(url=f"{ctx.guild.icon}")
  emb.set_footer(text=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
  msg=await ctx.channel.send(embed=emb, view=PartnerButtons())

class PartnerButtons(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)  
  @discord.ui.button(label = "Add you Server", style = discord.ButtonStyle.green, custom_id = "apply_button")
  async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
    await interaction.response.send_modal(PartnerModal())

class PartnerModal(ui.Modal, title="Add you Server"):
    name = ui.TextInput(label="Name", placeholder="Discord Name", style=discord.TextStyle.short, custom_id="1")
    guildid = ui.TextInput(label="Guild ID", placeholder="Your Guild ID", style=discord.TextStyle.short, custom_id="2")
    discord_server = ui.TextInput(label="Discord Server", placeholder="Server Link", style=discord.TextStyle.short, custom_id="3")

    async def on_submit(self, interaction: discord.Interaction) -> None:
      embed = discord.Embed(title="**New Partner**", description=f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n<:Partner:852778198693445682> Name: {self.name}\n☎️ Contact: {interaction.user.mention}\n<:Discord:852777697620918274> [**Discord Server**]({self.discord_server})\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬",color=int(get_config("colors")["embed_color"], 16))
      embed.set_thumbnail(url=f"{interaction.guild.icon}")
      embed.set_footer(text=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
      channel = interaction.guild.get_channel(850403390571544576)
      await channel.send(embed=embed)  
      embed = discord.Embed(description="Ein Neuer Partner wurde erstellt. Schau mal in <#850403390571544576>")
      await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def hpartner(ctx,*,message):
  emb=discord.Embed(title="How to Partner", description=f"{message}", color=int(get_config("colors")["embed_color"], 16))
  emb.set_author(name=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
  emb.set_thumbnail(url=f"{ctx.guild.icon}")
  emb.set_footer(text=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
  msg=await ctx.channel.send(embed=emb)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def price(ctx):
  emb=discord.Embed(title="How to order a Bot | PRICE", color=int(get_config("colors")["embed_color"], 16))
  emb.set_thumbnail(url=f"{ctx.guild.icon}")
  emb.add_field(name="<:right:850402507871748097> Clan Bot: <:ClanBot:850406953771466763> /Utility/System Bot", value="> `300+ Members Servers~` **or**\n> `2€* / Month`**/**`10€* Once`\n> <#850404789204025425> >> React with 📜 >> answer the Questions\n\n\n<:right:850402507871748097> _To be able to order / get a Discord Bot, you need to either have\n enough Server Members, or Invites, or pay._\n<:right:850402507871748097> _You can get **infinite** Discord Bots via **PAYMENT**_\n ⠀", inline=False)
  emb.add_field(name="NOTES", value="> _* We **don't** give refunds, pyments are taken and handled lika a_ [_donation_](https://paypal.me/LukasZangen?locale.x=de_DE)\n> _~ The Member Count does only work **ONCE**, per **USER** and\n> **ONCE** per **SERVER**_\n\n> _The bot is free for_ <#792390294686400522>.\n> _If you want to become a partner, take a look at the_ \n> <#850404789204025425> _Channel_", inline=False)
  emb.set_author(name=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
  emb.set_footer(text=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
  msg=await ctx.channel.send(embed=emb)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def botsmade(ctx,*,message):
  emb=discord.Embed(description=f"{message}", color=int(get_config("colors")["embed_color"], 16))
  emb.set_thumbnail(url=f"{ctx.guild.icon}")
  emb.set_author(name=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
  emb.set_footer(text=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
  msg=await ctx.channel.send(embed=emb)

@bot.command()
@commands.has_permissions(manage_messages=True)
async def news(ctx,*,message):
  await ctx.channel.send('@everyone')
  emb=discord.Embed(description=f"{message}", color=int(get_config("colors")["embed_color"], 16))
  emb.set_thumbnail(url=f"{ctx.guild.icon}")
  emb.set_author(name=f"{ctx.guild.name}")
  emb.set_footer(text=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
  msg=await ctx.channel.send(embed=emb)

# @bot.tree.command(name="Ticket", description="Erstelle ein Ticket")
# @commands.has_permissions(manage_messages=True)
# async def ticket(ctx:discord.Interaction):
#   emb=discord.Embed(title="Ticket-Support", description="Test", color=int(get_config("colors")["embed_color"], 16))
#   emb.set_footer(text=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
#   message=await ctx.channel.send(embed=emb)
#   await message.add_reaction('🎟️')   

#Apply-System#
@bot.command()
@commands.has_permissions(manage_messages=True)
async def order(ctx,*,message):
  emb=discord.Embed(title=f"**Order by:** `{ctx.guild.name}`", description=f"{message}", color=int(get_config("colors")["embed_color"], 16))
  emb.set_thumbnail(url=f"{ctx.guild.icon}")
  emb.set_author(name=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
  emb.set_footer(text=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
  message=await ctx.channel.send(embed=emb)
  await message.add_reaction('📜')                  

@bot.command()
async def create(ctx):
  global guildticket
  guildticket = ctx.guild
  embed = discord.Embed(title="**Create a Ticket / Application / Partnership**", description=f"<:right:850402507871748097> **If you __need help__, want to __apply__ or if you are having __Questions__, then please Open a Ticket!**\n\n<:right:850402507871748097> _**To open a Ticket click on the emoji down below!**_\n```diff\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬```\n<:Lukas:928361275879206912> **I need help with my Bot**\n> <:right:850402507871748097> Get help for your BOT\n\n❓ **I need general help**\n> <:right:850402507871748097> Get Help for anything of {ctx.guild.name}\n\n<:StaffMember:928360815713747004> **Apply as a Staff Member**\n> <:right:850402507871748097> Apply as a Staff Member for {ctx.guild.name}\n\n<:Partner:852778198693445682> **Apply as a Partner**\n> <:right:850402507871748097> Make a Partnership with {ctx.guild.name}\n\n<a:Code:928361576086528030> **Order a custom Bot**\n> <:right:850402507871748097> Order a payed custom Bot with Source Code!\n\n🚀 **Buy a Source Code**\n> <:right:850402507871748097> Order a payed custom Bot with Source Code!", color=int(get_config("colors")["embed_color"], 16))      
  embed.set_author(name=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
  embed.set_footer(text=f"{ctx.guild.name}",icon_url=f"{ctx.guild.icon}")
  embed.timestamp = datetime.utcnow()
  message = await ctx.send(embed=embed)
  await message.add_reaction('<:Lukas:928361275879206912>') 
  await message.add_reaction('❓') 
  await message.add_reaction('<:StaffMember:928360815713747004>') 
  await message.add_reaction('<:Partner:852778198693445682>') 
  await message.add_reaction('<a:Code:928361576086528030>')
  await message.add_reaction('🚀')

@bot.command()
async def test5(ctx, member: discord.Member = None):
    member = ctx.author if not member else member
    filename = f"transcript.txt"
    with open(filename, "w") as file:
        async for msg in ctx.channel.history(limit=None):
            file.write(f"{msg.created_at} - {msg.author.display_name}: {msg.clean_content}\n")
    with open(filename, "rb") as file:
        embed = discord.Embed(title=f"Log für den Ticket-Channel: `{ctx.channel.name}`", description=f"{member.mention}\n`{member}`\n`({ctx.channel.id})`")  
        embed.set_thumbnail(url=f"{member.display_avatar}")
        await member.send(f"Dein Ticket wurde von:`{ctx.author}` geschlossen! Hier dein Transcript", embed=embed)
        await asyncio.sleep(1)  
        await member.send(file=discord.File(file,filename=filename))

# @bot.command()
# async def close(ctx):
#   embed = discord.Embed(title="✅ Success!", description="Deleting Ticket in lass `3 Secounds`...\n\n _If not you can do it manually_", color=int(get_config("colors")["embed_color"], 16))
#   embed.set_thumbnail(url=f"{ctx.author.display_avatar}")
#   embed.set_footer(text=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
#   await ctx.send(embed=embed)
#   await asyncio.sleep(4)
#   await ctx.channel.delete() 

# @bot.command()
# async def write(ctx,*,text):
#   with open("test.json", "r") as f:
#     data = json.load(f)
#   data[ctx.guild.name]=text
#   with open("test.json", "w") as f:
#     json.dump(data, f)
#   await ctx.send(f"Ich habe **{text}** erfolgreich in die Json geschrieben")

# @bot.command()
# async def read(ctx):
#   with open("test.json", "r")as f:
#     data=json.load(f)
#   await ctx.send(data)  

@bot.command()
@commands.has_permissions(manage_messages=True)
async def apply(ctx,*,message):
  emb=discord.Embed(title=f"**Team-Apply by:** `{ctx.guild.name}`", description=f"{message}", color=int(get_config("colors")["embed_color"], 16))
  emb.set_thumbnail(url=f"{ctx.guild.icon}")
  emb.set_author(name=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
  emb.set_footer(text=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
  message=await ctx.channel.send(embed=emb)
  await message.add_reaction('📜')

@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    user = await bot.fetch_user(payload.user_id)
    channel = bot.get_channel(payload.channel_id)
    guild = bot.get_guild(payload.guild_id)
    message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
    reaction = discord.utils.get(message.reactions)

    ####################### TICKET #########################

    message_id = payload.message_id
    if message_id == 962660705268531320:
      guild_id = payload.guild_id
      guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)
    
      if str(reaction.emoji) == '🎟️':
        await reaction.remove(payload.member)
        channelexsits = discord.utils.get(guild.text_channels, name=user.name.lower().replace("#",""))
        if channelexsits:
          None
        else:
          if discord.utils.get(guild.categories, name="━┃🎫┃ Tickets┃🎫┃━") == None:
            category2 = await guild.create_category(name="━┃🎫┃ Tickets┃🎫┃━", position=2)
            ticket_channel = await guild.create_text_channel(f"🎫┃・ticket {user.name}", category=category2)
            await ticket_channel.set_permissions(user, read_messages=True, send_messages=True)
            await ticket_channel.send(f'{user.mention} | <@&850418386911232010> <@&850973608682717195> <@&928262177855524865>')
            embed = discord.Embed(description=f"> Hey {user.mention}!\n> You have created a ticket. How can we help you?\n\n> To close the ticket write `.close` in the chat.", color=int(get_config("colors")["embed_color"], 16))
            embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon}")
            embed.set_footer(text=f"{guild.name} | Ticket created", icon_url=f"{guild.icon}")
            embed.timestamp = datetime.utcnow()
            message = await ticket_channel.send(embed=embed)
          else:
            category = discord.utils.get(guild.categories, name="━┃🎫┃ Tickets┃🎫┃━")
            ticket_channel = await guild.create_text_channel(name=f"🎫┃・ticket {user.name}", category=category)
            await ticket_channel.set_permissions(user,read_messages=True, send_messages=True)
            await ticket_channel.send(f'{user.mention} | <@&850418386911232010> <@&850973608682717195> <@&928262177855524865>')
            embed = discord.Embed(description=f'> Hey {user.mention}!\n> You have created a ticket. How can we help you?\n\n> To close the ticket press the emoji `🔒` down below.', color=int(get_config("colors")["embed_color"], 16))
            embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon}")
            embed.set_footer(text=f"{guild.name} | Ticket created", icon_url=f"{guild.icon}")
            embed.timestamp = datetime.utcnow()
            message = await ticket_channel.send(embed=embed)  
            await message.add_reaction("🔒")
            embed = discord.Embed(title="", description=f"{user.mention} has creat a Ticket.\n\n**Channel:** {ticket_channel.mention}", color=int(get_config("colors")["embed_color"], 16))
            embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon}")
            embed.set_thumbnail(url=f"{user.display_avatar}")
            embed.set_footer(text=f"{guild.name} | Ticket created", icon_url=f"{guild.icon}") 
            channel = await bot.fetch_channel(log_channel)
            await channel.send(embed=embed)

            def check(reaction, member):
                        return (reaction.message.id == message.id and not member.bot)

            reaction, member = await bot.wait_for('reaction_add', check=check)
            if str(reaction.emoji) == "🔒":
              await reaction.remove(payload.member)  
              embed = discord.Embed(title="✅ Success!", description="Deleting Ticket in lass `3 Secounds`...\n\n _If not you can do it manually_", color=int(get_config("colors")["embed_color"], 16))
              embed.set_thumbnail(url=f"{user.display_avatar}")
              embed.set_footer(text=f"{guild.name}", icon_url=f"{guild.icon}")
              await ticket_channel.send(embed=embed)
              await asyncio.sleep(4)
              await ticket_channel.delete()
              embed = discord.Embed(title="✅ Success!", description="```Your Ticket was Successfully closed.\n\nYou can open a new Ticket in <#928730505778712607>.```", color=int(get_config("colors")["embed_color"], 16))
              embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon}")
              embed.set_thumbnail(url=f"{guild.icon}")
              embed.set_footer(text=f"{guild.name}", icon_url=f"{guild.icon}")  
              await user.send(embed=embed)  
              embed = discord.Embed(title="", description=f"{user.mention} has close a Ticket.\n\n**Channel:** {ticket_channel.mention}", color=int(get_config("colors")["embed_color"], 16))
              embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon}")
              embed.set_thumbnail(url=f"{user.display_avatar}")
              embed.set_footer(text=f"Ticket created", icon_url=f"{guild.icon}") 
              channel = await bot.fetch_channel(log_channel)
              await channel.send(embed=embed)

    ######################### APPLY ######################### 

    message_id = payload.message_id
    if message_id == 962506343435083786:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)

        if str(payload.emoji) == "📜":
            await reaction.remove(payload.member)
            role = discord.utils.get(guild.roles, name=get_config("roles")["customer"])
            if role is not None:
                member = discord.utils.find(lambda m: m.id == payload.user_id,
                                            guild.members)
                if member is not None:
                    await member.add_roles(role)
                    print("Rolle hinzugefügt")

                    def dm_check(m):
                      return m.author.id == user.id and m.guild is None

                    if True: # Ich hab kein bock alles ein nach links zu verschieben
                        embed = discord.Embed(title=f"**Order by** `{guild.name}`",description=f"Hey {user.mention}! Thanks for order a Bot\n```diff\n- Please tell us some Informations!```\nTo cancel your Bot-Order, type **__cancel__** in the chat.", color=int(get_config("colors")["embed_color"], 16))
                        embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon}")
                        embed.set_thumbnail(url=f"{guild.icon}")
                        embed.set_footer(text=f"{guild.name}", icon_url=f"{guild.icon}")
                        await user.send(embed=embed)
                        applyChannel = bot.get_channel(769114713048875008)
                        embed = discord.Embed(title="Bot Order", description="", color=int(get_config("colors")["embed_color"], 16))
                        embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon}")
                        embed.set_thumbnail(url=f"{guild.icon}")
                        questions = [["**1. |** `What should be the BOT NAME?`", "Question (1/8)"],
                        ["**2. |** `What should be the PREFIX?`", "Question (2/8)"],
                        ["**3. |** `What should be the AVATAR? (Avatar-link pls.)`", "Question (3/8)"],
                        ["**4. |** `What should be the EMBED COLOR? Pick one here:`\nhttps://htmlcolorcodes.com/", "Question (4/8)"],
                        ["**5. |** `What should be the BOT STATUS?`", "Question (5/8)"],
                        ["**6. |** `How many members does your server have? (Bots excluded)`", "Question (6/8)"],
                        ["**7. |** `In which Guild Should the Bot work (invite link)?`", "Question (7/8)"],
                        ["**8. |** `Do you have any wishes?`", "Question (8/8)"]]
                        answers = []
                        for x in questions:
                            embed = discord.Embed(title="Bot Order", color=int(get_config("colors")["embed_color"], 16))
                            embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon}")
                            embed.set_thumbnail(url=f"{guild.icon}")
                            embed.add_field(name=x[1], value=x[0], inline=False)
                            embed.set_footer(text=f"{guild.name}", icon_url=f"{guild.icon}")

                            await user.send(embed=embed)

                            answer = await bot.wait_for("message", check=dm_check)

                            if answer.content.lower().startswith("cancel"):
                                embed = discord.Embed(title="Bot Order", description="Your order was successfully **canceled**", color=int(get_config("colors")["embed_color"], 16))
                                embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon}")
                                embed.set_thumbnail(url=f"{guild.icon}")
                                embed.set_footer(text=f"{guild.name}", icon_url=f"{guild.icon}")
                                await user.send(embed=embed)
                                return

                            answers.append([x[0], answer.content])

                        embed = discord.Embed(title=f"**A new Bot Order from** {user.name}", description=f"**Bot Order from:** {user.mention}", color=int(get_config("colors")["embed_color"], 16))
                        embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon}")
                        embed.set_thumbnail(url=f"{guild.icon}")
                        embed.set_footer(text=f"{guild.name}", icon_url=f"{guild.icon}")
                        for x in answers:
                            embed.add_field(name=x[0], value=x[1], inline=False)

                        try:
                          mess = await applyChannel.send(embed=embed) 
                        except:
                          embed = discord.Embed(title="Bot Order", color=int(get_config("colors")["embed_color"], 16))
                          embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon}")
                          embed.add_field(name="Your order could not be sent!", value="> Please contact one of the team leaders", inline=False)
                          embed.set_thumbnail(url=f"{guild.icon}")
                          embed.set_footer(text=f"{guild.name}", icon_url=f"{guild.icon}")
                          await user.send(embed=embed)
                        else:
                          embed = discord.Embed(title=f"**Order by** `{guild.name}`", description=f"Hey {user.mention}! Thanks for order a Bot\n```diff\n+ Your Bot Order has been sent!```\nYour order is beeing reviewd. You will be messaged within the next 48 hours.", color=int(get_config("colors")["embed_color"], 16))
                          embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon}")
                          embed.set_thumbnail(url=f"{guild.icon}")
                          embed.set_footer(text=f"{guild.name}", icon_url=f"{guild.icon}")
                          await user.send(embed=embed)
                          await asyncio.sleep(1)
                          embed = discord.Embed(title=f"**A new Bot Order from** {user.name}", description=f"**Bot Order from:** {user.mention}", color=int(get_config("colors")["embed_color"], 16))
                          embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon}")
                          embed.set_thumbnail(url=f"{guild.icon}")
                          embed.set_footer(text=f"{guild.name}", icon_url=f"{guild.icon}")
                          for x in answers:
                              embed.add_field(name=x[0], value=x[1], inline=False)    
                          await user.send(embed=embed)         

                          await mess.add_reaction('✅')
                          await mess.add_reaction('❌')
                          def check(reaction, member):
                                      return (reaction.message.id == mess.id and not member.bot)

                          reaction, member = await bot.wait_for('reaction_add', check=check)
                          if str(reaction.emoji) == "✅":
                                  embed = discord.Embed(title=f"Bot Order `{user.name}`", description=f"Hey {user.mention}! Thanks for order a Bot\n```diff\n+ Your order has been accepted!```\n> Please open a ticket in the <#928730505778712607> with the things you want the bot to be able to do so that we can complete your order as soon as possible.", color=int(get_config("colors")["embed_color"], 16))
                                  embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon}")
                                  embed.set_thumbnail(url=f"{guild.icon}")
                                  embed.set_footer(text=f"{guild.name}", icon_url=f"{guild.icon}")  
                                  await user.send(embed=embed)
                          if str(reaction.emoji) == "❌":
                                  embed = discord.Embed(title="Bot Order", description="> Your order was not accepted!\n> You can try again to order a bot.", color=int(get_config("colors")["embed_color"], 16))
                                  embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon}")
                                  embed.set_thumbnail(url=f"{guild.icon}")
                                  embed.set_footer(text=f"{guild.name}", icon_url=f"{guild.icon}")  
                                  await user.send(embed=embed)

    message_id = payload.message_id
    if message_id == 929032620967362561:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)

        if str(payload.emoji) == "<:Partner:852778198693445682>":
            await reaction.remove(payload.member)
            role = discord.utils.get(guild.roles, name='👤・APPLICANTS・👤')
            if role is not None:
                member = discord.utils.find(lambda m: m.id == payload.user_id,
                                            guild.members)
                if member is not None:
                    await member.add_roles(role)
                    print("Rolle hinzugefügt")

                    def dm_check(m):
                      return m.author.id == user.id and m.guild is None

                    if True: # Ich hab kein bock alles ein nach links zu verschieben
                        embed = discord.Embed(title=f"**Partner-Apply by** `{guild.name}`",description=f"Hey {user.mention}! Thanks for opening an Partner-Apply\n```diff\n- Please tell us some Informations!```\nTo cancel your Partner-Apply, type **__cancel__** in the chat.", color=int(get_config("colors")["embed_color"], 16))
                        embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon}")
                        embed.set_thumbnail(url=f"{guild.icon}")
                        embed.set_footer(text=f"{guild.name}", icon_url=f"{guild.icon}")
                        await user.send(embed=embed)
                        applyChannel = bot.get_channel(769114713048875008)
                        embed = discord.Embed(title="Partner-Apply", description="", color=int(get_config("colors")["embed_color"], 16))
                        embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon}")
                        embed.set_thumbnail(url=f"{guild.icon}")
                        questions = [["**1. |** `What's your name?`", "Question (1/8)"],
                        ["**2. |** `How old are you?`", "Question (2/8)"],
                        ["**3. |** `Where are you from?`", "Question (3/8)"],
                        ["**4. |** `What is your Timezone?`", "Question (4/8)"],
                        ["**5. |** `What is your Discord Server (link)?`", "Question (5/8)"],
                        ["**6. |** `What can you offer us?`", "Question (6/8)"],
                        ["**7. |** `How do you expect that the Partnership will be like?`", "Question (7/8)"],
                        ["**8. |** `Do you fit the conditions?`", "Question (8/8)"]]
                        answers = []
                        for x in questions:
                            embed = discord.Embed(title="Partner-Apply", color=int(get_config("colors")["embed_color"], 16))
                            embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon}")
                            embed.set_thumbnail(url=f"{guild.icon}")
                            embed.add_field(name=x[1], value=x[0], inline=False)
                            embed.set_footer(text=f"{guild.name}", icon_url=f"{guild.icon}")

                            await user.send(embed=embed)

                            answer = await bot.wait_for("message", check=dm_check)

                            if answer.content.lower().startswith("cancel"):
                                embed = discord.Embed(title="Partner-Apply", description="Your Partner-Apply was successfully **canceled**", color=int(get_config("colors")["embed_color"], 16))
                                embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon}")
                                embed.set_thumbnail(url=f"{guild.icon}")
                                embed.set_footer(text=f"{guild.name}", icon_url=f"{guild.icon}")
                                await user.send(embed=embed)
                                return

                            answers.append([x[0], answer.content])

                        embed = discord.Embed(title=f"**A new Partner-Apply from** {user.name}", description=f"**Partner-Apply from:** {user.mention}", color=int(get_config("colors")["embed_color"], 16))
                        embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon}")
                        embed.set_thumbnail(url=f"{guild.icon}")
                        embed.set_footer(text=f"{guild.name}", icon_url=f"{guild.icon}")
                        for x in answers:
                            embed.add_field(name=x[0], value=x[1], inline=False)

                        try:
                          mess = await applyChannel.send(embed=embed)
                        except:
                          embed = discord.Embed(title="Partner-Apply", color=int(get_config("colors")["embed_color"], 16))
                          embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon}")
                          embed.add_field(name="Your order could not be sent!", value="> Please contact one of the team leaders", inline=False)
                          embed.set_thumbnail(url=f"{guild.icon}")
                          embed.set_footer(text=f"{guild.name}", icon_url=f"{guild.icon}")
                          await user.send(embed=embed)
                        else:
                          embed = discord.Embed(title="Partner-Apply", color=int(get_config("colors")["embed_color"], 16))
                          embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon}")
                          embed.add_field(name="Your order has been sent!", value="> Your Partner-Apply is beeing reviewd. You will be messaged within the next 48 hours.")
                          embed.set_thumbnail(url=f"{guild.icon}")
                          embed.set_footer(text=f"{guild.name}", icon_url=f"{guild.icon}")
                          await user.send(embed=embed)

                          await mess.add_reaction('✅')
                          await mess.add_reaction('❌')
                          def check(reaction, member):
                                      return (reaction.message.id == mess.id and not member.bot)

                          reaction, member = await bot.wait_for('reaction_add', check=check)
                          if str(reaction.emoji) == "✅":
                                  embed = discord.Embed(title="Partner-Apply", description="> Your Partner-Apply has been accepted!\n> You will get your role in the near future.", color=int(get_config("colors")["embed_color"], 16))
                                  embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon}")
                                  embed.set_thumbnail(url=f"{guild.icon}")
                                  embed.set_footer(text=f"{guild.name}", icon_url=f"{guild.icon}")  
                                  await user.send(embed=embed)
                          if str(reaction.emoji) == "❌":
                                  embed = discord.Embed(title="Partner-Apply", description="> Your Partner-Apply was not accepted!\n> You can try again to apply.", color=int(get_config("colors")["embed_color"], 16))
                                  embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon}")
                                  embed.set_thumbnail(url=f"{guild.icon}")
                                  embed.set_footer(text=f"{guild.name}", icon_url=f"{guild.icon}")  
                                  await user.send(embed=embed)

    message_id = payload.message_id
    if message_id == 852797577308536832:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)

        if str(payload.emoji) == "📜":
            await reaction.remove(payload.member)
            role = discord.utils.get(guild.roles, name='👤・APPLICANTS・👤')
            if role is not None:
                member = discord.utils.find(lambda m: m.id == payload.user_id,
                                            guild.members)
                if member is not None:
                    await member.add_roles(role)
                    print("Rolle hinzugefügt")

                    def dm_check(m):
                      return m.author.id == user.id and m.guild is None

                    if True: # Ich hab kein bock alles ein nach links zu verschieben
                        embed = discord.Embed(title=f"**Team-Apply by:** `{guild.name}`",description=f"Hey {user.mention}! Thanks for opening an Team-Apply\n```diff\n- Please tell us some Informations!```\nTo cancel your Team-Apply, type **__cancel__** in the chat.", color=int(get_config("colors")["embed_color"], 16))
                        embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon}")
                        embed.set_thumbnail(url=f"{guild.icon}")
                        embed.set_footer(text=f"{guild.name}", icon_url=f"{guild.icon}")
                        await user.send(embed=embed)
                        applyChannel = bot.get_channel(769114713048875008)
                        embed = discord.Embed(title="Team-Apply", description="", color=int(get_config("colors")["embed_color"], 16))
                        embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon}")
                        embed.set_thumbnail(url=f"{guild.icon}")
                        questions = [["**1. |** `What's your name?`", "Question (1/7)"],
                        ["**2. |** `How old are you?`", "Question (2/7)"],
                        ["**3. |** `Where are you from?`", "Question (3/7)"],
                        ["**4. |** `What is your Timezone?`", "Question (4/7)"],
                        ["**5. |** `How often are you online + how much time can you spend on this DC?`", "Question (5/7)"],
                        ["**6. |** `Do you have experience, if so which and how much?`", "Question (6/7)"],
                        ["**7. |** `How do you expect that the work will be for you?`", "Question (7/7)"]]
                        answers = []
                        for x in questions:
                            embed = discord.Embed(title="Team-Apply", color=int(get_config("colors")["embed_color"], 16))
                            embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon}")
                            embed.set_thumbnail(url=f"{guild.icon}")
                            embed.add_field(name=x[1], value=x[0], inline=False)
                            embed.set_footer(text=f"{guild.name}", icon_url=f"{guild.icon}")

                            await user.send(embed=embed)

                            answer = await bot.wait_for("message", check=dm_check)

                            if answer.content.lower().startswith("cancel"):
                                embed = discord.Embed(title="Mod-Apply", description="Your apply was successfully **canceled**", color=int(get_config("colors")["embed_color"], 16))
                                embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon}")
                                embed.set_thumbnail(url=f"{guild.icon}")
                                embed.set_footer(text=f"{guild.name}", icon_url=f"{guild.icon}")
                                await user.send(embed=embed)
                                return

                            answers.append([x[0], answer.content])

                        embed = discord.Embed(title=f"**A new Team-Apply from** {user.name}", description=f"**Team-Apply from:** {user.mention}", color=int(get_config("colors")["embed_color"], 16))
                        embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon}")
                        embed.set_thumbnail(url=f"{guild.icon}")
                        embed.set_footer(text=f"{guild.name}", icon_url=f"{guild.icon}")
                        for x in answers:
                            embed.add_field(name=x[0], value=x[1], inline=False)

                        try:
                          mess = await applyChannel.send(embed=embed)
                        except:
                          embed = discord.Embed(title="Team-Apply", color=int(get_config("colors")["embed_color"], 16))
                          embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon}")
                          embed.add_field(name="Your order could not be sent!", value="> Please contact one of the team leaders", inline=False)
                          embed.set_thumbnail(url=f"{guild.icon}")
                          embed.set_footer(text=f"{guild.name}", icon_url=f"{guild.icon}")
                          await user.send(embed=embed)
                        else:
                          embed = discord.Embed(title="Team-Apply", color=int(get_config("colors")["embed_color"], 16))
                          embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon}")
                          embed.add_field(name="Your order has been sent!", value="> Your apply is beeing reviewd. You will be messaged within the next 48 hours.")
                          embed.set_thumbnail(url=f"{guild.icon}")
                          embed.set_footer(text=f"{guild.name}", icon_url=f"{guild.icon}")
                          await user.send(embed=embed)
                          await mess.add_reaction('✅')
                          await mess.add_reaction('❌')

                          def check(reaction, member):
                                      return (reaction.message.id == mess.id and not member.bot)

                          reaction, member = await bot.wait_for('reaction_add', check=check)
                          if str(reaction.emoji) == "✅":
                                  embed = discord.Embed(title="Team-Apply", description="> Your Team-Apply has been accepted!\n> You will get your role in the near future.", color=int(get_config("colors")["embed_color"], 16))
                                  embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon}")
                                  embed.set_thumbnail(url=f"{guild.icon}")
                                  embed.set_footer(text=f"{guild.name}", icon_url=f"{guild.icon}")  
                                  await user.send(embed=embed)
                          if str(reaction.emoji) == "❌":
                                  embed = discord.Embed(title="Team-Apply", description="> Your Team-Apply was not accepted!\n> You can try again to apply.", color=int(get_config("colors")["embed_color"], 16))
                                  embed.set_author(name=f"{guild.name}", icon_url=f"{guild.icon}")
                                  embed.set_thumbnail(url=f"{guild.icon}")
                                  embed.set_footer(text=f"{guild.name}", icon_url=f"{guild.icon}")  
                                  await user.send(embed=embed) 
        
    ######################### REACTIONS #########################

    message_id = payload.message_id
    if message_id == 806498136796430336:
      guild_id = payload.guild_id
      guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

      if payload.emoji.name == "FSK14":
        role = discord.utils.get(guild.roles, name='12 - 14 Jahre')
        embed = discord.Embed(description="> You have successfully assigned yourself to role `12 - 14 Years`!\n\n_With best regards_\n**Team Lukas Services**", color=int(get_config("colors")["embed_color"], 16))
        embed.set_author(name=f"{guild.name}", icon_url=guild.icon)
        embed.set_thumbnail(url=guild.icon)
        embed.set_footer(text=f"{guild.name}", icon_url=guild.icon)
        await user.send(embed=embed)
      elif payload.emoji.name == 'FSK16':
        role = discord.utils.get(guild.roles, name='15 - 17 Jahre')
        embed = discord.Embed(description="> You have successfully assigned yourself to role `15 - 17 Years`!\n\n_With best regards_\n**Team Lukas Services**", color=int(get_config("colors")["embed_color"], 16))
        embed.set_author(name=f"{guild.name}", icon_url=guild.icon)
        embed.set_thumbnail(url=guild.icon)
        embed.set_footer(text=f"{guild.name}", icon_url=guild.icon)
        await user.send(embed=embed)
      elif payload.emoji.name == 'FSK18':
        role = discord.utils.get(guild.roles, name='18+ Jahre')
        embed = discord.Embed(description="> You have successfully assigned yourself to role `18+ Years`!\n\n_With best regards_\n**Team Lukas Services**", color=int(get_config("colors")["embed_color"], 16))
        embed.set_author(name=f"{guild.name}", icon_url=guild.icon)
        embed.set_thumbnail(url=guild.icon)
        embed.set_footer(text=f"{guild.name}", icon_url=guild.icon)
        await user.send(embed=embed)
      else:
        role = discord.utils.get(guild.roles, name=payload.emoji.name)
      if role is not None:
        member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
        if member is not None:
          await member.add_roles(role)
          print("Rolle hinzugefügt")
        else:
          print("Member not found")
      else:
        print("Role not found")

    message_id = payload.message_id
    if message_id == 806525636759781427:
      guild_id = payload.guild_id
      guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

      if payload.emoji.name == '🙍‍♂️':
        role = discord.utils.get(guild.roles, name='role2')
        embed = discord.Embed(description="> You have successfully assigned yourself to role `role2`!\n\n_With best regards_\n**Team Lukas Services**", color=int(get_config("colors")["embed_color"], 16))
        embed.set_author(name=f"{guild.name}", icon_url=guild.icon)
        embed.set_thumbnail(url=guild.icon)
        embed.set_footer(text=f"{guild.name}", icon_url=guild.icon)
        await user.send(embed=embed)
      elif payload.emoji.name == '🙍‍♀️':
        role = discord.utils.get(guild.roles, name='role1')
        embed = discord.Embed(description="> You have successfully assigned yourself to role `role1`!\n\n_With best regards_\n**Team Lukas Services**", color=int(get_config("colors")["embed_color"], 16))
        embed.set_author(name=f"{guild.name}", icon_url=guild.icon)
        embed.set_thumbnail(url=guild.icon)
        embed.set_footer(text=f"{guild.name}", icon_url=guild.icon)
        await user.send(embed=embed)
      elif payload.emoji.name == '🦄':
        role = discord.utils.get(guild.roles, name='role3ers')
        embed = discord.Embed(description="> You have successfully assigned yourself to role `role3ers`!\n\n_With best regards_\n**Team Lukas Services**", color=int(get_config("colors")["embed_color"], 16))
        embed.set_author(name=f"{guild.name}", icon_url=guild.icon)
        embed.set_thumbnail(url=guild.icon)
        embed.set_footer(text=f"{guild.name}", icon_url=guild.icon)
        await user.send(embed=embed)
      else:
        role = discord.utils.get(guild.roles, name=payload.emoji.name)
      if role is not None:
        member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
        if member is not None:
          await member.add_roles(role)
          print("Rolle hinzugefügt")
        else:
          print("Member not found")
      else:
        print("Role not found")

    message_id = payload.message_id
    if message_id == 806525864816672798:
      guild_id = payload.guild_id
      guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

      if payload.emoji.name == '🇩🇪':
        role = discord.utils.get(guild.roles, name='German')
        embed = discord.Embed(title="Self Role", description="> You have successfully assigned yourself to role `German`!\n\n_With best regards_\n**Team Lukas Services**", color=int(get_config("colors")["embed_color"], 16))
        embed.set_author(name=f"{guild.name}", icon_url=guild.icon)
        embed.set_thumbnail(url=guild.icon)
        embed.set_footer(text=f"{guild.name}", icon_url=guild.icon)
        await user.send(embed=embed)
      elif payload.emoji.name == '🇬🇧':
        role = discord.utils.get(guild.roles, name='English')
        embed = discord.Embed(title="Self Role", description="> You have successfully assigned yourself to role `English`!\n\n_With best regards_\n**Team Lukas Services**", color=int(get_config("colors")["embed_color"], 16))
        embed.set_author(name=f"{guild.name}", icon_url=guild.icon)
        embed.set_thumbnail(url=guild.icon)
        embed.set_footer(text=f"{guild.name}", icon_url=guild.icon)
        await user.send(embed=embed)
      elif payload.emoji.name == '🚫':
        role = discord.utils.get(guild.roles, name='Other language')
        embed = discord.Embed(title="Self Role", description="> You have successfully assigned yourself to role `Other language`!\n\n_With best regards_\n**Team Lukas Services**", color=int(get_config("colors")["embed_color"], 16))
        embed.set_author(name=f"{guild.name}", icon_url=guild.icon)
        embed.set_thumbnail(url=guild.icon)
        embed.set_footer(text=f"{guild.name}", icon_url=guild.icon)
        await user.send(embed=embed)
      else:
        role = discord.utils.get(guild.roles, name=payload.emoji.name)
      if role is not None:
        member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
        if member is not None:
          await member.add_roles(role)
          print("Rolle hinzugefügt")
        else:
          print("Member not found")
      else:
        print("Role not found")

@bot.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    user = await bot.fetch_user(payload.user_id)
    
    message_id = payload.message_id
    if message_id == 806498136796430336:
      guild_id = payload.guild_id
      guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

      if payload.emoji.name == 'FSK14':
        role = discord.utils.get(guild.roles, name='12 - 14 Jahre')
        embed = discord.Embed(title="Self Role", description="> You have successfully removed roll `12 - 14 Years`!\n\n_With best regards_\n**Team Lukas Services**", color=int(get_config("colors")["embed_color"], 16))
        embed.set_author(name=f"{guild.name}", icon_url=guild.icon)
        embed.set_thumbnail(url=guild.icon)
        embed.set_footer(text=f"{guild.name}", icon_url=guild.icon)
        await user.send(embed=embed)
      elif payload.emoji.name == 'FSK16':
        role = discord.utils.get(guild.roles, name='15 - 17 Jahre')
        embed = discord.Embed(title="Self Role", description="> You have successfully removed roll `15 - 17 Years`!\n\n_With best regards_\n**Team Lukas Services**", color=int(get_config("colors")["embed_color"], 16))
        embed.set_author(name=f"{guild.name}", icon_url=guild.icon)
        embed.set_thumbnail(url=guild.icon)
        embed.set_footer(text=f"{guild.name}", icon_url=guild.icon)
        await user.send(embed=embed)
      elif payload.emoji.name == 'FSK18':
        role = discord.utils.get(guild.roles, name='18+ Jahre')
        embed = discord.Embed(title="Self Role", description="> You have successfully removed roll `18+ Years`!\n\n_With best regards_\n**Team Lukas Services**", color=int(get_config("colors")["embed_color"], 16))
        embed.set_author(name=f"{guild.name}", icon_url=guild.icon)
        embed.set_thumbnail(url=guild.icon)
        embed.set_footer(text=f"{guild.name}", icon_url=guild.icon)
        await user.send(embed=embed)
      else:
        role = discord.utils.get(guild.roles, name=payload.emoji.name)

      if role is not None:
        member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
        if member is not None:
          await member.remove_roles(role)
          print("Rolle entfernt")
        else:
          print("Member not found")
      else:
        print("Role not found")

    message_id = payload.message_id
    if message_id == 806525636759781427:
      guild_id = payload.guild_id
      guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

      if payload.emoji.name == '🙍‍♂️':
        role = discord.utils.get(guild.roles, name='role2')
        embed = discord.Embed(title="Self Role", description="> You have successfully removed roll `role2`!\n\n_With best regards_\n**Team Lukas Services**", color=int(get_config("colors")["embed_color"], 16))
        embed.set_author(name=f"{guild.name}", icon_url=guild.icon)
        embed.set_thumbnail(url=guild.icon)
        embed.set_footer(text=f"{guild.name}", icon_url=guild.icon)
        await user.send(embed=embed)
      elif payload.emoji.name == '🙍‍♀️':
        role = discord.utils.get(guild.roles, name='role1')
        embed = discord.Embed(title="Self Role", description="> You have successfully removed roll `role1`!\n\n_With best regards_\n**Team Lukas Services**", color=int(get_config("colors")["embed_color"], 16))
        embed.set_author(name=f"{guild.name}", icon_url=guild.icon)
        embed.set_thumbnail(url=guild.icon)
        embed.set_footer(text=f"{guild.name}", icon_url=guild.icon)
        await user.send(embed=embed)
      elif payload.emoji.name == '🦄':
        role = discord.utils.get(guild.roles, name='role3ers')
        embed = discord.Embed(title="Self Role", description="> You have successfully removed roll `role3erse`!\n\n_With best regards_\n**Team Lukas Services**", color=int(get_config("colors")["embed_color"], 16))
        embed.set_author(name=f"{guild.name}", icon_url=guild.icon)
        embed.set_thumbnail(url=guild.icon)
        embed.set_footer(text=f"{guild.name}", icon_url=guild.icon)
        await user.send(embed=embed)
      else:
        role = discord.utils.get(guild.roles, name=payload.emoji.name)

      if role is not None:
        member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
        if member is not None:
          await member.remove_roles(role)
          print("Rolle entfernt")
        else:
          print("Member not found")
      else:
        print("Role not found")

    message_id = payload.message_id
    if message_id == 806525864816672798:
      guild_id = payload.guild_id
      guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

      if payload.emoji.name == '🇩🇪':
        role = discord.utils.get(guild.roles, name='German')
        embed = discord.Embed(title="Self Role", description="> You have successfully removed roll `German`!\n\n_With best regards_\n**Team Lukas Services**", color=int(get_config("colors")["embed_color"], 16))
        embed.set_author(name=f"{guild.name}", icon_url=guild.icon)
        embed.set_thumbnail(url=guild.icon)
        embed.set_footer(text=f"{guild.name}", icon_url=guild.icon)
        await user.send(embed=embed)
      elif payload.emoji.name == '🇬🇧':
        role = discord.utils.get(guild.roles, name='English')
        embed = discord.Embed(title="Self Role", description="> You have successfully removed roll `English`!\n\n_With best regards_\n**Team Lukas Services**", color=int(get_config("colors")["embed_color"], 16))
        embed.set_author(name=f"{guild.name}", icon_url=guild.icon)
        embed.set_thumbnail(url=guild.icon)
        embed.set_footer(text=f"{guild.name}", icon_url=guild.icon)
        await user.send(embed=embed)
      elif payload.emoji.name == '🚫':
        role = discord.utils.get(guild.roles, name='Other language')
        embed = discord.Embed(title="Self Role", description="> You have successfully removed roll `Other language`!\n\n_With best regards_\n**Team Lukas Services**", color=int(get_config("colors")["embed_color"], 16))
        embed.set_author(name=f"{guild.name}", icon_url=guild.icon)
        embed.set_thumbnail(url=guild.icon)
        embed.set_footer(text=f"{guild.name}", icon_url=guild.icon)
        await user.send(embed=embed)
      else:
        role = discord.utils.get(guild.roles, name=payload.emoji.name)

      if role is not None:
        member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
        if member is not None:
          await member.remove_roles(role)
          print("Rolle entfernt")
        else:
          print("Member not found")
      else:
        print("Role not found")

#Giveaway Command#
def convert(time):
  pos = ["s","m","h","d"]

  time_dict = {"s" : 1, "m" : 60, "h" : 3600, "d": 3600*24}

  unit = time[-1]

  if unit not in pos:
    return -1
  try:
    val = int(time[:-1])
  except:
    return -2

  return val * time_dict[unit]

@bot.command()
@commands.has_permissions(kick_members=True)
async def giveaway(ctx):
  embed = discord.Embed(title="🎉 Giveaway 🎉", description="Let's start with this giveaway! Answer these questions within 15 seconds!", color=int(get_config("colors")["embed_color"], 16))
  embed.set_author(name=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
  embed.set_footer(text=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
  await ctx.send(embed=embed)
  questions = [["Which channel should it be hosted in?"], 
              ["What should be the duration of the giveaway? (s|m|h|d)"], 
              ["What is the prize of the giveaway?"]]

  answers = []

  def check(m):
    return m.author == ctx.author and m.channel == ctx.channel

  for x in questions:
    embed = discord.Embed(title="🎉 Giveaway 🎉", description=x[0], color=int(get_config("colors")["embed_color"], 16))
    embed.set_author(name=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}") 
    embed.set_footer(text=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")                                         
    await ctx.send(embed=embed)

    try:
      msg = await bot.wait_for('message', timeout=25.0, check=check)
    except asyncio.TimeoutError:
      embed = discord.Embed(title="🎉 Giveaway 🎉", description="You didn\'t answer in time, please be quicker next time!", color=int(get_config("colors")["embed_color"], 16))
      embed.set_author(name=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
      embed.set_footer(text=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")                      
      await ctx.send(embed=embed)
      return
    else: 
      answers.append(msg.content)

  try:
    c_id = int(answers[0][2:-1])
  except:
    await ctx.send(f"You didn't mention a channel properly. Do it like this {ctx.channel.mention} next time.")
    return

  channel = bot.get_channel(c_id)

  time = convert(answers[1])
  if time == -1:
    embed = discord.Embed(title=f"🎉 Giveaway 🎉", description=f"You didn't answer with a proper unit. Use (s|m|h|d) next time!", color=int(get_config("colors")["embed_color"], 16))
    embed.set_author(name=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
    embed.set_footer(text=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
    await ctx.send(embed=embed)
    return
  elif time == -2:
    embed = discord.Embed(title="🎉 Giveaway 🎉", description=f"The time just be an integer. Please enter an integer next time.", color=int(get_config("colors")["embed_color"], 16))
    embed.set_author(name=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
    embed.set_footer(text=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
    await ctx.send(embed=embed)
    return
  
  prize = answers[2]
  
  embed = discord.Embed(title="🎉 Giveaway 🎉", description=f"The giveaway will be in {channel.mention} and will last {answers[1]} seconds!", color=int(get_config("colors")["embed_color"], 16))
  embed.set_author(name=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
  embed.set_footer(text=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
  await ctx.send(embed=embed)
  
  embed = discord.Embed(title="🎉 Giveaway 🎉", color = int(get_config("colors")["embed_color"], 16))
  embed.set_author(name=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
  embed.set_thumbnail(url=f"{ctx.guild.icon}")
  embed.add_field(name="Prize:", value=f"{prize}", inline=False)
  embed.add_field(name="Hosted by:", value = ctx.author.mention, inline=True)
  embed.add_field(name="Ends:", value=f"{answers[1]} from now!", inline=True)
  embed.set_footer(text=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
  my_msg = await channel.send(embed = embed)

  await my_msg.add_reaction("🎉")

  await asyncio.sleep(time)

  new_msg = await channel.fetch_message(my_msg.id)

  reaction = new_msg.reactions[0]
  users = []
  async for user in reaction.users():
      users.append(user)
  users.pop(users.index(bot.user))

  winner = random.choice(users)
  embed = discord.Embed(title="🎉 Giveaway 🎉", description=f"Congratulations! You won the prize: `{prize}`!\n Please make a ticket in <#850403438168899584> so that we can send you the gift.", color=int(get_config("colors")["embed_color"], 16))
  embed.set_author(name=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
  embed.set_footer(text=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
  await winner.send(embed=embed)
  embed = discord.Embed(title="🎉 Giveaway 🎉", description=f"Congratulations! {winner.mention} won the prize: `{prize}`!", color=int(get_config("colors")["embed_color"], 16))
  embed.set_author(name=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
  embed.set_footer(text=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
  await channel.send(embed=embed)

@bot.command()
@commands.has_permissions(kick_members=True)
async def reroll(ctx, channel: discord.TextChannel, id_: int):
    try:
        new_msg = await channel.fetch_message(id_)
    except discord.NotFound:
        embed = discord.Embed(title="🎉 Giveaway 🎉", description="The ID that was entered was incorrect, make sure you have entered the correct giveaway message ID.", color=int(get_config("colors")["embed_color"], 16))
        embed.set_author(name=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
        embed.set_thumbnail(url=f"{ctx.guild.icon}")
        embed.set_footer(text=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
        await ctx.send(embed=embed)
        return
    
    users = await new_msg.reactions[0].users().flatten()
    users.remove(bot.user)
    
    winner = random.choice(users)

    embed = discord.Embed(title="🎉 Giveaway 🎉", description=f"Congratulations the new winner is: {winner.mention} for the giveaway rerolled!", color=int(get_config("colors")["embed_color"], 16))
    embed.set_author(name=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
    embed.set_thumbnail(url=f"{ctx.guild.icon}")
    embed.set_footer(text=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
    await channel.send(embed=embed)

    embed = discord.Embed(title="🎉 Giveaway 🎉", description=f"Congratulations!\n You are the new winner!\n Please make a ticket in <#850403438168899584> so that we can send you the gift.", color=int(get_config("colors")["embed_color"], 16))
    embed.set_author(name=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
    embed.set_footer(text=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
    await winner.send(embed=embed)


@bot.command()
async def pi(ctx):
  embed = discord.Embed(title='This is the Number"`pi`"', description=f'`{math.pi}`')
  embed.set_thumbnail(url=f"{ctx.guild.icon}")
  embed.set_footer(text=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
  await ctx.send(embed=embed)

class ContextMemberKick(app_commands.ContextMenu):
  def __init__(self):
    super().__init__(callback=self.getMemberKick, name="Get Kick Member") 
    self.add_check(self.check_if_it_is_me)
    self.error(self.error_handler)

  async def getMemberKick(self, interaction: discord.Interaction, member: discord.Member):
    await interaction.user.kick()
    await interaction.response.send_message(f"{member.mention} wurde vom Server gekickt", ephemeral=True)

  def check_if_it_is_me(self, interaction: discord.Interaction) -> bool:
    return interaction.user.id == 440251035773173767
  
  async def error_handler(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
    await interaction.response.send_message("Sie sind nicht der Administrator", ephemeral=True)

class ContextMessage(app_commands.ContextMenu):
  def __init__(self):
     super().__init__(callback=self.getMessageAuthor, name="Get Message Author") 
     self.add_check(self.check_if_it_is_me)
     self.error(self.error_handler)

  async def getMessageAuthor(self, interaction: discord.Interaction, message: discord.Message):
    await interaction.response.send_message(message.author, ephemeral=True)

  def check_if_it_is_me(self, interaction: discord.Interaction) -> bool:
    return interaction.user.id == 440251035773173767
  
  async def error_handler(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
    await interaction.response.send_message("Sie sind nicht der Administrator", ephemeral=True)

class ContextReportMessage(app_commands.ContextMenu):
  def __init__(self):
     super().__init__(callback=self.getMessage, name="Report Message") 

  async def getMessage(self, interaction: discord.Interaction, message: discord.Message):
    await interaction.response.send_modal(ReportModal(original_message=message))
    
class ReportModal(ui.Modal, title="Report Massage"):
    reason = ui.TextInput(label="Reason", style=discord.TextStyle.long, required=False, max_length=200, custom_id="1")
    
    def __init__(self, original_message=None):
        super().__init__()
        self.original_message = original_message

    async def on_submit(self, interaction: discord.Interaction) -> None:
      await interaction.response.send_message("Nachricht wurde gesendet!", ephemeral=True)
      guild = interaction.guild
      category_name = "Reports"  # Name der Kategorie, in der der neue Kanal erstellt wird
      category = discord.utils.get(guild.categories, name=category_name)
      if category is None:
        category = await guild.create_category(category_name)
        
      channel_name = "Report-" + str(interaction.user.id)  # Name des neuen Kanals
      new_channel = await guild.create_text_channel(channel_name, category=category)
      
      channel = await bot.fetch_channel(new_channel.id)
      if self.original_message:
        original_author = self.original_message.author.mention  # Der Autor der ursprünglichen Nachricht wird aufgezeichnet
        await channel.send(f"Report-Grund: {self.reason.value}\nUrsprüngliche Nachricht: {self.original_message.jump_url}\nUrsprünglicher Autor: {original_author}")
      else:
        await channel.send(f"Report-Grund: {self.reason.value}")


class ContextMember(app_commands.ContextMenu):
  def __init__(self):
     super().__init__(callback=self.getMember, name="Get Member") 

  async def getMember(self, interaction: discord.Interaction, member: discord.Member):
    await interaction.response.send_message(member.name, ephemeral=True)

class ContextUserInfo(app_commands.ContextMenu):
  def __init__(self):
     super().__init__(callback=self.getMember, name="User Information") 

  async def getMember(self, interaction: discord.Interaction, member: discord.Member = None):
    if not member:
            member = ctx.author
        
    roles = [role.mention for role in member.roles[1:]] if len(member.roles) > 1 else ["None"]

    embed = discord.Embed(title=f"**Information about - {member.name}**", color=member.color)
    embed.set_author(name=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
    embed.set_thumbnail(url=member.display_avatar)
    embed.add_field(name="TAG:", value=f"`{member}`\n{member.mention}", inline=True)
    embed.add_field(name="ID:", value=f"`{member.id}`", inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=True)
    embed.add_field(name="Is a BOT:", value=f"`{member.bot}`", inline=True)
    embed.add_field(name="Server Joined", value=f"`{member.joined_at.strftime('%d.%m.%Y, %H:%M:%S')}`", inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=True)
    embed.add_field(name="Discord Joined", value=f"`{member.created_at.strftime('%d.%m.%Y, %H:%M:%S')}`", inline=True)
    embed.add_field(name="Presence:", value=f"`{member.activity}`", inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=True)
    embed.add_field(name="Status:", value=f"`{member.status}`", inline=True)
    embed.add_field(name="Rollen", value=", ".join(roles), inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)    

class ContextUserAvatar(app_commands.ContextMenu):
  def __init__(self):
     super().__init__(callback=self.getMember, name="User Avatar") 

  async def getMember(self, interaction: discord.Interaction, member: discord.Member = None):
    if not member:
            member = ctx.author

    embed = discord.Embed(title="**Avatar**", color=member.color)
    embed.set_author(name=f"{member.name}", icon_url=f"{member.display_avatar}")
    embed.set_image(url=member.display_avatar)
    await interaction.response.send_message(embed=embed, ephemeral=True)    

bot.tree.add_command(ContextReportMessage())
bot.tree.add_command(ContextUserAvatar())
bot.tree.add_command(ContextUserInfo())
bot.tree.add_command(ContextMessage())
bot.tree.add_command(ContextMember())
bot.tree.add_command(ContextMemberKick())

############################################
####            Apply-System            ####
############################################ 

conn = sqlite3.connect('poll.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS poll (question text, upvotes integer, downvotes integer)''')

conn.commit()

@bot.tree.command(name="suggest", description="Create a Suggestion")
async def suggest(interaction: discord.Interaction):
   await interaction.response.send_modal(SuggestionModal())

class SuggestionModal(ui.Modal, title="Create a Suggestion"):
    question = ui.TextInput(label="Your Suggestion", placeholder="Write your Suggestion", style=discord.TextStyle.short, custom_id="1")

    async def on_submit(self, interaction: discord.Interaction) -> None:
        upvote = 0
        downvote = 0
        question = self.question.value
        name = interaction.user.name
        thumbnail = interaction.user.display_avatar.url
        c.execute("INSERT INTO poll VALUES (?, ?, ?, ?, ?)", (question, 0, 0, name, thumbnail))
        conn.commit()
        embed = discord.Embed(description=f"> {question}", color=int(get_config("colors")["embed_color"], 16))
        embed.set_thumbnail(url=f"{thumbnail}")
        embed.add_field(name=f"👍 __**Up Votes**__", value=f"```0 Votes```", inline=True)
        embed.add_field(name=f"👎 __**Down Votes**__", value=f"```0 Votes```", inline=True)
        embed.set_author(name=f"{name} Suggestion", icon_url=f"{interaction.guild.icon}")
        embed.set_footer(text=f"Want to suggest something? Simply type /suggest in this Channel!", icon_url=f"{interaction.guild.icon}")
        channel = interaction.guild.get_channel(1084107686074908752)
        await channel.send(embed=embed, view=SuggestionButtons(question, upvote, downvote))
        embed = discord.Embed(description=f"{interaction.user.mention} Your Suggestion was created")
        await interaction.response.send_message(embed=embed, ephemeral=True)

class SuggestionButtons(discord.ui.View):
    def __init__(self, question: str, upvote: int, downvote: int):
        super().__init__(timeout=None)
        self.question = question
        self.voter = {}
        self.upvote = upvote
        self.downvote = downvote

    @discord.ui.button(label="", emoji="<:Check:772401517759037441>", style=discord.ButtonStyle.grey, custom_id="poll1_button")
    async def poll1(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        if user_id in self.voter:
            if self.voter[user_id] == 1: # Nutzer hat bereits upvoted, also wird der Vote entfernt
                self.voter.pop(user_id)
                self.upvote -= 1
            else: # Nutzer hat bereits downvoted, also wird der downvote entfernt und upvote hinzugefügt
                self.voter[user_id] = 1
                self.downvote -= 1
                self.upvote += 1
        else: # Nutzer hat noch nicht abgestimmt, also wird upvote hinzugefügt
            self.voter[user_id] = 1
            self.upvote += 1
        c.execute("UPDATE poll SET upvotes = ? WHERE question = ?", (self.upvote, self.question))
        c.execute("UPDATE poll SET downvotes = ? WHERE question = ?", (self.downvote, self.question))
        c.execute("SELECT name, thumbnail FROM poll WHERE question = ?", (self.question,))
        conn.commit()
        c.execute("SELECT name, thumbnail FROM poll WHERE question = ?", (self.question,))
        result = c.fetchone()
        name, thumbnail = result[0], result[1]
        c.execute("SELECT upvotes, downvotes FROM poll WHERE question = ?", (self.question,))
        row = c.fetchone()
        self.upvote = row[0]
        self.downvote = row[1]
        embed = discord.Embed(description=f"> {self.question}", color=int(get_config("colors")["embed_color"], 16))
        embed.set_thumbnail(url=thumbnail)
        embed.add_field(name=f"👍 __**Up Votes**__", value=f"```{self.upvote} Votes```", inline=True)
        embed.add_field(name=f"👎 __**Down Votes**__", value=f"```{self.downvote} Votes```", inline=True)
        embed.set_author(name=f"{name} Suggestion", icon_url=f"{interaction.guild.icon}")
        embed.set_footer(text=f"Want to suggest something? Simply type /suggest in this Channel!", icon_url=f"{interaction.guild.icon}")
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="", emoji="<:Cross:772401517667680276>", style=discord.ButtonStyle.grey, custom_id="poll2_button")
    async def poll2(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        if user_id in self.voter:
            if self.voter[user_id] == 1: # Nutzer hat bereits downvoted, also wird der Vote entfernt
                self.voter.pop(user_id)
                self.downvote -= 1
            else: # Nutzer hat bereits upvoted, also wird der upvote entfernt und downvote hinzugefügt
                self.voter[user_id] = 1
                self.upvote -= 1
                self.downvote += 1
        else: # Nutzer hat noch nicht abgestimmt, also wird downvote hinzugefügt
            self.voter[user_id] = 1
            self.downvote += 1
        c.execute("UPDATE poll SET upvotes = ? WHERE question = ?", (self.upvote, self.question))
        c.execute("UPDATE poll SET downvotes = ? WHERE question = ?", (self.downvote, self.question))
        conn.commit()
        c.execute("SELECT name, thumbnail FROM poll WHERE question = ?", (self.question,))
        result = c.fetchone()
        name, thumbnail = result[0], result[1]
        c.execute("SELECT upvotes, downvotes FROM poll WHERE question = ?", (self.question,))
        row = c.fetchone()
        self.upvote = row[0]
        self.downvote = row[1]
        embed = discord.Embed(description=f"> {self.question}", color=int(get_config("colors")["embed_color"], 16))
        embed.set_thumbnail(url=thumbnail)
        embed.add_field(name=f"👍 __**Up Votes**__", value=f"```{self.upvote} Votes```", inline=True)
        embed.add_field(name=f"👎 __**Down Votes**__", value=f"```{self.downvote} Votes```", inline=True)
        embed.set_author(name=f"{name} Suggestion", icon_url=f"{interaction.guild.icon}")
        embed.set_footer(text=f"Want to suggest something? Simply type /suggest in this Channel!", icon_url=f"{interaction.guild.icon}")
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Who voted?", emoji="❓", style=discord.ButtonStyle.blurple, custom_id="poll3_button")
    async def poll3(self, interaction: discord.Interaction, button: discord.ui.Button): 
      voters = [f"<@{voter}>" for voter in self.voter]
      if voters:
        embed = discord.Embed(title="❓**Who has voted?**❓", color=int(get_config("colors")["embed_color"], 16)) 
        embed.add_field(name="Voters", value=f"{', '.join(voters)}") 
        embed.set_footer(text=f"Want to suggest something? Simply type /suggest in this Channel!", icon_url=f"{interaction.guild.icon}")
        await interaction.response.send_message(embed=embed, ephemeral=True)
      else:
        embed = discord.Embed(description="No one has voted yet.", color=int(get_config("colors")["embed_color"], 16))  
        embed.set_footer(text=f"Want to suggest something? Simply type /suggest in this Channel!", icon_url=f"{interaction.guild.icon}")
        await interaction.response.send_message(embed=embed, ephemeral=True) 

@bot.command()
async def verify(ctx, *, message):
  embed = discord.Embed(title="Server Rules", description=f"{message}", color=int(get_config("colors")["embed_color"], 16))
  embed.set_thumbnail(url=f"{ctx.guild.icon}")
  embed.set_author(name=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
  embed.set_image(url="https://media.discordapp.net/attachments/790720708208623656/1073965671857270784/Banner_Rules.png")
  embed.set_footer(text=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
  message = await ctx.send(embed=embed, view=VerifyButtons())

class VerifyButtons(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)  
  @discord.ui.button(label="Accept the Rules", style = discord.ButtonStyle.green, custom_id = "verify_button")
  async def verify(self, interaction: discord.Interaction, button: discord.ui.Button):
    author = interaction.user
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5)) # Erstelle einen zufälligen 5-stelligen Captcha-Text
    image = ImageCaptcha().generate_image(captcha_text) # Generiere ein Captcha-Bild mit dem Text

    # Konvertiere das Bild in Bytes
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='PNG')
    image_bytes.seek(0)

    try:
        embed = discord.Embed(title=f"{interaction.guild.name}", description=f"{interaction.user.mention}, You have accepted the rule, please verify yourself. Verification was started in the DM. If you are verified, you will get access to the server.", color=0x2b2d31)
        embed.set_footer(text=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        channel = await interaction.user.create_dm()  # Öffne die DM des Benutzers
    except discord.Forbidden:
        await interaction.response.send_message("I couldn't send you a direct message. Please make sure you have direct messages enabled for members of this server.", ephemeral=True)
        return
    except Exception as e:
        await interaction.response.send_message(f"An error occurred while trying to send you a direct message: {e}", ephemeral=True)
        return

    channel = await interaction.user.create_dm() # Öffne die DM des Benutzers
    embed = discord.Embed(title=f"Welcome to `{interaction.guild.name}`", color=0x2b2d31)
    embed.add_field(name="Captcha", value="Please complete the captcha below to again acces to the Server.\n**NOTE:** This is **Case Sensitive**.\n\n**Why?**\nThis is to protect the Server against\nmalicious raids using automated Bots.\n\n**Your Captcha:**")
    embed.set_image(url=f"attachment://{captcha_text}.png")
    embed.set_footer(text=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
    message = await channel.send(embed=embed, file=discord.File(fp=image_bytes, filename=f'{captcha_text}.png'))

    def check(msg):
        return msg.author == interaction.user and msg.content == captcha_text # Überprüfe, ob die Nachricht vom richtigen Mitglied kommt und den richtigen Code enthält

    try:
        msg = await bot.wait_for('message', timeout=120.0, check=check) # Warte auf die Eingabe des Mitglieds
    except asyncio.TimeoutError: # Wenn die Zeit abläuft
        await channel.send("Timeout. Please try again.") # Sende eine Fehlermeldung
        return

    role = discord.utils.get(interaction.guild.roles, name="✅・Verified・✅") # Ändern Sie "Verified" in den Namen der Rolle, die Sie vergeben möchten
    await interaction.user.add_roles(role) # Vergeben Sie die Rolle
    embed = discord.Embed(title="Thank you!", description="You have been given access to our Server!", color=0x2b2d31)
    embed.set_footer(text=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
    await channel.send(embed=embed) # Sende eine Bestätigungsnachricht
    embed = discord.Embed(title=f"{interaction.guild.name}", description=f"{interaction.user.mention}, wurde erfolgreich verifiziert.", color=0x2b2d31)
    embed.set_thumbnail(url=f"{interaction.user.display_avatar.url}")
    embed.set_footer(text=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
    await bot.get_guild(595056528105406464).get_channel(1084488342655205466).send(embed=embed) # Ändern Sie CHANNEL_ID in die ID des Kanals, in dem Sie die Bestätigungsnachricht erhalten möchten

@bot.tree.command(name="apply", description="Apply for...")
async def applytest(interaction: discord.Interaction):
  embed = discord.Embed(title="Get your own Bot now!", color=int(get_config("colors")["embed_color"], 16))
  embed.set_author(name=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
  embed.set_thumbnail(url=f"{interaction.guild.icon}")
  embed.add_field(name="__**Basic**__", value="\n```✅ 24/7 Available\n✅ Moderation\n✅ Application & Tickets```", inline=False)
  embed.add_field(name="__**Advanced**__", value="\n```✅ 24/7 Available\n✅ Advanced & Automated Moderation\n✅ Application & Tickets\n✅ Fast Support\n✅ Economy & Games```", inline=False)
  embed.add_field(name="__**Professional**__", value="\n```✅ 24/7 Available\n✅ Advanced & Automated Moderation\n✅ More advanced Application & Tickets\n✅ High priority Support\n✅ Economy & Games\n✅ More Custom Functions```", inline=True)
  embed.set_footer(text=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
  await interaction.response.send_message(embed=embed, view=applymenu())

class applymenu(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    options=[
        discord.SelectOption(label="📜 - Basic", value=1,),
        discord.SelectOption(label="📜 - Advanced", value=2),
        discord.SelectOption(label="📜 - Professional", value=3),
    ]

    @discord.ui.select(placeholder="Erstell ein Ticket", min_values=1, max_values=1, options=options, custom_id="selectmenu")
    async def select(self, interaction: discord.Interaction, select):
      if select.values[0] == "1":  
        def dm_check(m):
          return m.author.id == interaction.user.id and m.guild is None
        await interaction.response.send_message(f"Schau in deine DM {interaction.user.mention}", ephemeral = True)  
        embed = discord.Embed(title=f"**Order by** `{interaction.guild.name}`",description=f"Hey {interaction.user.mention}! Thanks for order a Bot\n```diff\n- Please tell us some Informations!```\nTo cancel your Bot-Order, type **__cancel__** in the chat.", color=int(get_config("colors")["embed_color"], 16))
        embed.set_author(name=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
        embed.set_thumbnail(url=f"{interaction.guild.icon}")
        embed.set_footer(text=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
        await interaction.user.send(embed=embed)
        applyChannel = bot.get_channel(769114713048875008)
        embed = discord.Embed(title="Bewerbung", description="", color=int(get_config("colors")["embed_color"], 16))
        embed.set_author(name=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
        embed.set_thumbnail(url=f"{interaction.guild.icon}")
        questions = [["**1. |** `What should be the BOT NAME?`", "Question (1/8)"],
        ["**2. |** `What should be the PREFIX?`", "Question (2/8)"],
        ["**3. |** `What should be the AVATAR? (Avatar-link pls.)`", "Question (3/8)"],
        ["**4. |** `What should be the EMBED COLOR? Pick one here:` [HTML Color](https://htmlcolorcodes.com/)", "Question (4/8)"],
        ["**5. |** `What should be the BOT STATUS?`", "Question (5/8)"],
        ["**6. |** `How many members does your server have? (Bots excluded)`", "Question (6/8)"],
        ["**7. |** `In which Guild Should the Bot work (invite link)?`", "Question (7/8)"],
        ["**8. |** `Do you have any wishes?`", "Question (8/8)"]]
        answers = []
        for x in questions:
          embed = discord.Embed(title="Bewerbung", color=int(get_config("colors")["embed_color"], 16))
          embed.set_author(name=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
          embed.set_thumbnail(url=f"{interaction.guild.icon}")
          embed.add_field(name=x[1], value=x[0], inline=False)
          embed.set_footer(text=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")

          await interaction.user.send(embed=embed)

          answer = await bot.wait_for("message", check=dm_check)
          
          if answer.content.lower().startswith("cancel"):
            embed = discord.Embed(title="Bewerbung", description="Deine Bewerbung wurde Erfolgreich **abgebrochen**", color=int(get_config("colors")["embed_color"], 16))
            embed.set_author(name=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
            embed.set_thumbnail(url=f"{interaction.guild.icon}")
            embed.set_footer(text=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
            await interaction.user.send(embed=embed)
            return

          answers.append([x[0], answer.content])

        embed = discord.Embed(title=f"**Eine Neue Bewerbung** {interaction.user.name}", description=f"**Bewerbung von:** {interaction.user.mention}", color=int(get_config("colors")["embed_color"], 16))
        embed.set_author(name=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
        embed.set_thumbnail(url=f"{interaction.guild.icon}")
        embed.set_footer(text=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
        for x in answers:
          embed.add_field(name=x[0], value=x[1], inline=False)

        try:
            mess = await applyChannel.send(embed=embed)
        except:
          embed = discord.Embed(title="Bewerbung", color=int(get_config("colors")["embed_color"], 16))
          embed.set_author(name=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
          embed.add_field(name="Deine Bewerbung konnte nciht gesendet werden!", value="> Bitte kontaktiere unser Team", inline=False)
          embed.set_thumbnail(url=f"{interaction.guild.icon}")
          embed.set_footer(text=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
          await interaction.user.send(embed=embed)
        else:
          embed = discord.Embed(title=f"**Bewerbung ** `{interaction.guild.name}`", description=f"Hey {interaction.user.mention}! Danke für deine Bewerbung\n```diff\n+ Deine bewerbung wirde gesendet!```\nDeine Bewerbung wird gerade überprüft. Wir werden dich innerhalb der nächsten 48 Stunden benachrichtigen.", color=int(get_config("colors")["embed_color"], 16))
          embed.set_author(name=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
          embed.set_thumbnail(url=f"{interaction.guild.icon}")
          embed.set_footer(text=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
          await interaction.user.send(embed=embed) 
          await mess.add_reaction('✅')
          await mess.add_reaction('❌')

          def check(reaction, member):
                      return (reaction.message.id == mess.id and not member.bot)

          reaction, member = await bot.wait_for('reaction_add', check=check)
          if str(reaction.emoji) == "✅":
            embed = discord.Embed(title="Team-Apply", description="> Your Team-Apply has been accepted!\n> You will get your role in the near future.", color=int(get_config("colors")["embed_color"], 16))
            embed.set_author(name=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
            embed.set_thumbnail(url=f"{interaction.guild.icon}")
            embed.set_footer(text=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")  
            await interaction.user.send(embed=embed)
          if str(reaction.emoji) == "❌":
            embed = discord.Embed(title="Team-Apply", description="> Your Team-Apply was not accepted!\n> You can try again to apply.", color=int(get_config("colors")["embed_color"], 16))
            embed.set_author(name=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
            embed.set_thumbnail(url=f"{interaction.guild.icon}")
            embed.set_footer(text=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")  
            await interaction.user.send(embed=embed) 

      elif select.values[0] == "2":  
        def dm_check(m):
          return m.author.id == interaction.user.id and m.guild is None
        await interaction.response.send_message(f"Schau in deine DM {interaction.user.mention}", ephemeral = True)  
        embed = discord.Embed(title=f"**Order by** `{interaction.guild.name}`",description=f"Hey {interaction.user.mention}! Thanks for order a Bot\n```diff\n- Please tell us some Informations!```\nTo cancel your Bot-Order, type **__cancel__** in the chat.", color=int(get_config("colors")["embed_color"], 16))
        embed.set_author(name=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
        embed.set_thumbnail(url=f"{interaction.guild.icon}")
        embed.set_footer(text=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
        await interaction.user.send(embed=embed)
        applyChannel = bot.get_channel(769114713048875008)
        embed = discord.Embed(title="Bot Order", description="", color=int(get_config("colors")["embed_color"], 16))
        embed.set_author(name=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
        embed.set_thumbnail(url=f"{interaction.guild.icon}")
        questions = [["**1. |** `What should be the BOT NAME?`", "Question (1/8)"],
        ["**2. |** `What should be the PREFIX?`", "Question (2/8)"],
        ["**3. |** `What should be the AVATAR? (Avatar-link pls.)`", "Question (3/8)"],
        ["**4. |** `What should be the EMBED COLOR? Pick one here:`\nhttps://htmlcolorcodes.com/", "Question (4/8)"],
        ["**5. |** `What should be the BOT STATUS?`", "Question (5/8)"],
        ["**6. |** `How many members does your server have? (Bots excluded)`", "Question (6/8)"],
        ["**7. |** `In which Guild Should the Bot work (invite link)?`", "Question (7/8)"],
        ["**8. |** `Do you have any wishes?`", "Question (8/8)"]]
        answers = []
        for x in questions:
          embed = discord.Embed(title="Bewerbung", color=int(get_config("colors")["embed_color"], 16))
          embed.set_author(name=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
          embed.set_thumbnail(url=f"{interaction.guild.icon}")
          embed.add_field(name=x[1], value=x[0], inline=False)
          embed.set_footer(text=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")

          await interaction.user.send(embed=embed)

          answer = await bot.wait_for("message", check=dm_check)
          
          if answer.content.lower().startswith("cancel"):
            embed = discord.Embed(title="Bewerbung", description="Deine Bewerbung wurde Erfolgreich **abgebrochen**", color=int(get_config("colors")["embed_color"], 16))
            embed.set_author(name=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
            embed.set_thumbnail(url=f"{interaction.guild.icon}")
            embed.set_footer(text=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
            await interaction.user.send(embed=embed)
            return

          answers.append([x[0], answer.content])

        embed = discord.Embed(title=f"**Eine Neue Bewerbung** {interaction.user.name}", description=f"**Bewerbung von:** {interaction.user.mention}", color=int(get_config("colors")["embed_color"], 16))
        embed.set_author(name=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
        embed.set_thumbnail(url=f"{interaction.guild.icon}")
        embed.set_footer(text=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
        for x in answers:
          embed.add_field(name=x[0], value=x[1], inline=False)

        try:
          mess = await applyChannel.send(embed=embed) 
        except:
          embed = discord.Embed(title="Bewerbung", color=int(get_config("colors")["embed_color"], 16))
          embed.set_author(name=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
          embed.add_field(name="Deine Bewerbung konnte nciht gesendet werden!", value="> Bitte kontaktiere unser Team", inline=False)
          embed.set_thumbnail(url=f"{interaction.guild.icon}")
          embed.set_footer(text=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
          await interaction.user.send(embed=embed)
        else:
          embed = discord.Embed(title=f"**Bewerbung ** `{interaction.guild.name}`", description=f"Hey {interaction.user.mention}! Danke für deine Bewerbung\n```diff\n+ Deine bewerbung wirde gesendet!```\nDeine Bewerbung wird gerade überprüft. Wir werden dich innerhalb der nächsten 48 Stunden benachrichtigen.", color=int(get_config("colors")["embed_color"], 16))
          embed.set_author(name=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
          embed.set_thumbnail(url=f"{interaction.guild.icon}")
          embed.set_footer(text=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
          await interaction.user.send(embed=embed) 
          await mess.add_reaction('✅')
          await mess.add_reaction('❌')

          def check(reaction, member):
                      return (reaction.message.id == mess.id and not member.bot)

          reaction, member = await bot.wait_for('reaction_add', check=check)
          if str(reaction.emoji) == "✅":
            embed = discord.Embed(title="Team-Apply", description="> Your Team-Apply has been accepted!\n> You will get your role in the near future.", color=int(get_config("colors")["embed_color"], 16))
            embed.set_author(name=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
            embed.set_thumbnail(url=f"{interaction.guild.icon}")
            embed.set_footer(text=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")  
            await interaction.user.send(embed=embed)
          if str(reaction.emoji) == "❌":
            embed = discord.Embed(title="Team-Apply", description="> Your Team-Apply was not accepted!\n> You can try again to apply.", color=int(get_config("colors")["embed_color"], 16))
            embed.set_author(name=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
            embed.set_thumbnail(url=f"{interaction.guild.icon}")
            embed.set_footer(text=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")  
            await interaction.user.send(embed=embed)

      elif select.values[0] == "3":  
        def dm_check(m):
          return m.author.id == interaction.user.id and m.guild is None
        await interaction.response.send_message(f"Schau in deine DM {interaction.user.mention}", ephemeral = True)  
        embed = discord.Embed(title=f"**Order by** `{interaction.guild.name}`",description=f"Hey {interaction.user.mention}! Thanks for order a Bot\n```diff\n- Please tell us some Informations!```\nTo cancel your Bot-Order, type **__cancel__** in the chat.", color=int(get_config("colors")["embed_color"], 16))
        embed.set_author(name=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
        embed.set_thumbnail(url=f"{interaction.guild.icon}")
        embed.set_footer(text=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
        await interaction.user.send(embed=embed)
        applyChannel = bot.get_channel(769114713048875008)
        embed = discord.Embed(title="Bot Order", description="", color=int(get_config("colors")["embed_color"], 16))
        embed.set_author(name=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
        embed.set_thumbnail(url=f"{interaction.guild.icon}")
        questions =[
        ["**1. |** `What should be the BOT NAME?`", "Question (1/8)"],
        ["**2. |** `What should be the PREFIX?`", "Question (2/8)"],
        ["**3. |** `What should be the AVATAR? (Avatar-link pls.)`", "Question (3/8)"],
        ["**4. |** `What should be the EMBED COLOR? Pick one here:`\nhttps://htmlcolorcodes.com/", "Question (4/8)"],
        ["**5. |** `What should be the BOT STATUS?`", "Question (5/8)"],
        ["**6. |** `How many members does your server have? (Bots excluded)`", "Question (6/8)"],
        ["**7. |** `In which Guild Should the Bot work (invite link)?`", "Question (7/8)"],
        ["**8. |** `Do you have any wishes?`", "Question (8/8)"]]
        answers = []
        for x in questions:
          embed = discord.Embed(title="Bewerbung", color=int(get_config("colors")["embed_color"], 16))
          embed.set_author(name=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
          embed.set_thumbnail(url=f"{interaction.guild.icon}")
          embed.add_field(name=x[1], value=x[0], inline=False)
          embed.set_footer(text=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")

          await interaction.user.send(embed=embed)

          answer = await bot.wait_for("message", check=dm_check)
          
          if answer.content.lower().startswith("cancel"):
            embed = discord.Embed(title="Bewerbung", description="Deine Bewerbung wurde Erfolgreich **abgebrochen**", color=int(get_config("colors")["embed_color"], 16))
            embed.set_author(name=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
            embed.set_thumbnail(url=f"{interaction.guild.icon}")
            embed.set_footer(text=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
            await interaction.user.send(embed=embed)
            return

          answers.append([x[0], answer.content])

        embed = discord.Embed(title=f"**Eine Neue Bewerbung** {interaction.user.name}", description=f"**Bewerbung von:** {interaction.user.mention}", color=int(get_config("colors")["embed_color"], 16))
        embed.set_author(name=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
        embed.set_thumbnail(url=f"{interaction.guild.icon}")
        embed.set_footer(text=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
        for x in answers:
          embed.add_field(name=x[0], value=x[1], inline=False)

        try:
          mess = await applyChannel.send(embed=embed) 
        except:
          embed = discord.Embed(title="Bewerbung", color=int(get_config("colors")["embed_color"], 16))
          embed.set_author(name=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
          embed.add_field(name="Deine Bewerbung konnte nciht gesendet werden!", value="> Bitte kontaktiere unser Team", inline=False)
          embed.set_thumbnail(url=f"{interaction.guild.icon}")
          embed.set_footer(text=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
          await interaction.user.send(embed=embed)
        else:
          embed = discord.Embed(title=f"**Bewerbung ** `{interaction.guild.name}`", description=f"Hey {interaction.user.mention}! Danke für deine Bewerbung\n```diff\n+ Deine bewerbung wirde gesendet!```\nDeine Bewerbung wird gerade überprüft. Wir werden dich innerhalb der nächsten 48 Stunden benachrichtigen.", color=int(get_config("colors")["embed_color"], 16))
          embed.set_author(name=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
          embed.set_thumbnail(url=f"{interaction.guild.icon}")
          embed.set_footer(text=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
          await interaction.user.send(embed=embed) 
          await mess.add_reaction('✅')
          await mess.add_reaction('❌')

          def check(reaction, member):
                      return (reaction.message.id == mess.id and not member.bot)

          reaction, member = await bot.wait_for('reaction_add', check=check)
          if str(reaction.emoji) == "✅":
            embed = discord.Embed(title="Team-Apply", description="> Your Team-Apply has been accepted!\n> You will get your role in the near future.", color=int(get_config("colors")["embed_color"], 16))
            embed.set_author(name=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
            embed.set_thumbnail(url=f"{interaction.guild.icon}")
            embed.set_footer(text=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")  
            await interaction.user.send(embed=embed)
          if str(reaction.emoji) == "❌":
            embed = discord.Embed(title="Team-Apply", description="> Your Team-Apply was not accepted!\n> You can try again to apply.", color=int(get_config("colors")["embed_color"], 16))
            embed.set_author(name=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
            embed.set_thumbnail(url=f"{interaction.guild.icon}")
            embed.set_footer(text=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")  
            await interaction.user.send(embed=embed)

@bot.tree.command(name="feedback", description="Give us your feedback!")
async def feedback(interaction: discord.Interaction):
  await interaction.response.send_modal(FeedbackModal())  

class FeedbackModal(ui.Modal, title="Crerate a Feedback"):
    feddback = ui.TextInput(label="Feedback", placeholder="Your Feedback", style=discord.TextStyle.long, custom_id="1")

    async def on_submit(self, interaction: discord.Interaction) -> None:
      embed = discord.Embed(description=f"{interaction.user.mention} | {interaction.user.name}#{interaction.user.discriminator}", color=int(get_config("colors")["embed_color"], 16))
      embed.add_field(name=f"**Feedback:**", value=f"```{self.feddback}```", inline=False)
      embed.set_author(name=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
      embed.set_thumbnail(url=f"{interaction.user.avatar}")
      embed.set_footer(text=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}") 
      channel = interaction.guild.get_channel(850405946236076032)
      mess = await channel.send(embed=embed)
      await mess.add_reaction('✅')
      embed = discord.Embed(description=f"{interaction.user.mention} thank you for your Feedback!",color=int(get_config("colors")["embed_color"], 16))
      await interaction.response.send_message(embed=embed, ephemeral = True)
      
conn = sqlite3.connect('rabattcodes.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS rabattcodes
                  (code text PRIMARY KEY, user_id integer)''')

def create_code(length=10):
    characters = string.ascii_uppercase + string.digits
    code = ''.join(random.choice(characters) for i in range(length))
    return code

def save_code(code, user_id):
    cursor.execute('INSERT INTO rabattcodes VALUES (?, ?)', (code, user_id))
    conn.commit()

@bot.tree.command(name="generade_rabattcode", description="Generade a Rabatt Code")
async def generate_code_for_user(interaction: discord.Interaction, user: discord.User):
    code = create_code()
    save_code(code, user.id)
    embed = discord.Embed(description=f"Rabattcode für {user.mention}: `{code}`", color=int(get_config("colors")["embed_color"], 16))
    await interaction.response.send_message(embed=embed, ephemeral = True)

@bot.tree.command(name="create_rabattcode", description="Create a Rabatt-Code")
async def generate_code(interaction: discord.Interaction):
    code = create_code()
    save_code(code, interaction.user.id)
    embed = discord.Embed(description=f"Dein Rabattcode: `{code}`", color=int(get_config("colors")["embed_color"], 16))
    await interaction.response.send_message(embed=embed, ephemeral = True)

@bot.tree.command(name="user_rabattcode", description="Rabatt-Code von dir oder einem anderen User anzeigen")
async def get_code_for_user(interaction: discord.Interaction, user: discord.User):
    cursor.execute('SELECT code FROM rabattcodes WHERE user_id = ?', (user.id,))
    code = cursor.fetchone()
    if code:
        embed = discord.Embed(description=f"Rabattcode für {user.mention}: `{code[0]}`", color=int(get_config("colors")["embed_color"], 16))
        await interaction.response.send_message(embed=embed, ephemeral = True)
    else:
        embed = discord.Embed(description=f"Kein Rabattcode gefunden für {user.mention}.", color=int(get_config("colors")["embed_color"], 16))
        await interaction.response.send_message(embed=embed, ephemeral = True)

@bot.command()
async def use_code(ctx, code):
    cursor.execute('SELECT user_id FROM rabattcodes WHERE code = ?', (code,))
    user_id = cursor.fetchone()
    if user_id and user_id[0] == ctx.author.id:
        cursor.execute('DELETE FROM rabattcodes WHERE code = ?', (code,))
        conn.commit()
        embed = discord.Embed(description=f"Rabattcode erfolgreich verwendet.", color=int(get_config("colors")["embed_color"], 16))
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description=f"Der Rabattcode ist ungültig oder gehört nicht zu dir.", color=int(get_config("colors")["embed_color"], 16))
        await ctx.send(embed=embed)

if os.path.isfile("channels.json"):
    with open('channels.json', encoding='utf-8') as f:
        channels = json.load(f)
else:
    channels = {}
    with open('channels.json', 'w') as f:
        json.dump(channels, f, indent=4)

tempchannels = []

@bot.command(pass_context=True)
async def add(ctx, channelid):
    if ctx.author.bot:
        return
    if ctx.author.guild_permissions.administrator:
        if channelid:
            for vc in ctx.guild.voice_channels:
                if vc.id == int(channelid):
                    if str(ctx.channel.guild.id) not in channels:
                        channels[str(ctx.channel.guild.id)] = []
                    channels[str(ctx.channel.guild.id)].append(int(channelid))
                    with open('channels.json', 'w') as f:
                        json.dump(channels, f, indent=4)
                    embed = discord.Embed(color=int(get_config("colors")["embed_color"], 16)) 
                    embed.set_author(name="TempChannel", icon_url=f"{ctx.guild.icon}")
                    embed.add_field(name="🔄 **CHANNEL UPDATE**", value="> `{}` is now a TempChannel.".format(vc.name), inline=True)
                    embed.set_footer(text=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")   
                    await ctx.send(embed=embed)
                    return
            embed = discord.Embed(color=int(get_config("colors")["embed_color"], 16))
            embed.set_author(name="TempChannel", icon_url=f"{ctx.guild.icon}")  
            embed.add_field(name='ℹ️ **INFORMATION**', value="> `{}` is not a voice channel.".format(channelid))    
            embed.set_footer(text=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")  
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(color=int(get_config("colors")["embed_color"], 16))
            embed.set_author(name="TempChannel", icon_url=f"{ctx.guild.icon}")
            embed.add_field(name='ℹ️ **INFORMATION**', value=f"> Please enter a ChannelID.")
            embed.set_footer(text=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(color=int(get_config("colors")["embed_color"], 16))
        embed.set_author(name="TempChannel", icon_url=f"{ctx.guild.icon}")
        embed.add_field(name='ℹ️ **INFORMATION**', value=f'> You need administrator permissions to do this.')
        embed.set_footer(text=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
        await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def remove(ctx, channelid):
    if ctx.author.bot:
        return
    if ctx.author.guild_permissions.administrator:
        if channelid:
            guildS = str(ctx.channel.guild.id)
            channelidI = int(channelid)
            for vc in ctx.guild.voice_channels:
                if vc.id == int(channelid):
                    if channels[guildS]:
                        if channelidI in channels[guildS]:
                            channels[guildS].remove(channelidI)
                            with open('channels.json', 'w') as f:
                                json.dump(channels, f, indent=4)
                                embed = discord.Embed(color=int(get_config("colors")["embed_color"], 16))
                                embed.set_author(name="TempChannel", icon_url=f"{ctx.guild.icon}")
                                embed.add_field(name="🔄 **CHANNEL UPDATE**", value="> `{}` is no longer a TempChannel.".format(vc.name), inline=True)
                                embed.set_footer(text=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")    
                                await ctx.send(embed=embed)
                                return
                        else:
                            embed = discord.Embed(color=int(get_config("colors")["embed_color"], 16))
                            embed.set_author(name="TempChannel", icon_url=f"{ctx.guild.icon}")
                            embed.add_field(name='ℹ️ **INFORMATION**', value=f"> This channel doesn't exist here.")
                            embed.set_footer(text=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
                            await ctx.send(embed=embed)
                            return
            embed = discord.Embed(color=int(get_config("colors")["embed_color"], 16))
            embed.set_author(name="TempChannel", icon_url=f"{ctx.guild.icon}") 
            embed.add_field(name='ℹ️ **INFORMATION**', value=f"> You don't have any TempChannels yet.")    
            embed.set_footer(text=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")          
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(color=int(get_config("colors")["embed_color"], 16))
            embed.set_author(name="TempChannel", icon_url=f"{ctx.guild.icon}")
            embed.add_field(name='ℹ️ **INFORMATION**', value=f'> No ChannelID given.')
            embed.set_footer(text=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
            await ctx.send(embed=embed)
    else:
        embed = discord.Embed(color=int(get_config("colors")["embed_color"], 16))
        embed.set_author(name="TempChannel", icon_url=f"{ctx.guild.icon}")
        embed.add_field(name='ℹ️ **INFORMATION**', value=f'> You need administrator permissions to do this.')
        embed.set_footer(text=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
        await ctx.send(embed=embed)

@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel:
        if isTempChannel(before.channel):
            bchan = before.channel
            if len(bchan.members) == 0:
                await bchan.delete(reason="No member in tempchannel")
    if after.channel:
        if isJoinHub(after.channel):
            overwrite = discord.PermissionOverwrite()
            overwrite.manage_channels = True
            overwrite.move_members = True
            name = "{} Room".format(member.name)
            output = await after.channel.clone(name=name, reason="Joined in joinhub")
            if output:
                tempchannels.append(output.id)
                await output.set_permissions(member, overwrite=overwrite)
                await member.move_to(output, reason="Created tempvoice")

async def getChannel(guild, name):
    for channel in guild.voice_channels:
        if name in channel.name:
            return channel
    return None


def isJoinHub(channel):
    if channels[str(channel.guild.id)]:
        if channel.id in channels[str(channel.guild.id)]:
            return True
    return False


def isTempChannel(channel):
    if channel.id in tempchannels:
        return True
    else:
        return False

class GiveawayView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.entered_users = []

    async def select_winner(self,interaction: discord.Interaction, message_id):
        await asyncio.sleep(self.duration)
        message = await self.interaction.channel.fetch_message(message_id)
        users = [user for user in await message.reactions[0].users().flatten() if not user.bot]
        if users:
            winner = random.choice(users)
            await self.interaction.channel.send(f"Congratulations {winner.mention}! You won the **{self.prize}** giveaway!")
        else:
            await self.interaction.channel.send("Nobody entered the giveaway. Better luck next time!")
        self.stop()

class GiveawayButton(discord.ui.Button):
    def __init__(self, duration: int, prize: str):
        super().__init__(style=discord.ButtonStyle.green, label="Enter Giveaway", custom_id="giveaway")
        self.duration = duration * 60
        self.prize = prize

    async def callback(self, interaction: discord.Interaction):
        view: GiveawayView = self.view
        if interaction.user not in view.entered_users:
            view.entered_users.append(interaction.user)
            await interaction.response.send_message(f"You entered the giveaway for **{self.prize}**!", ephemeral=True)
        else:
            await interaction.response.send_message("You have already entered the giveaway.", ephemeral=True)

@bot.command()
async def gstart(ctx: commands.Context, duration: int, prize: str):
    # create giveaway embed and message
    embed = discord.Embed(title="🎉 GIVEAWAY 🎉", description=f"React with 🎉 to enter for a chance to win **{prize}**!", color=0x2b2d31)
    embed.add_field(name="Duration", value=f"{duration} minutes")
    embed.set_footer(text=f"Giveaway by {ctx.author.display_name}")
    giveaway_msg = await ctx.send(embed=embed, view=GiveawayView())
    await giveaway_msg.add_reaction("🎉")
    view = giveaway_msg.view
    view.duration = duration * 60
    view.prize = prize
    view.add_item(GiveawayButton(duration, prize))
    await view.wait()
    await view.select_winner(giveaway_msg.id)

@bot.tree.command(description="Generate your own Passwort")
async def generate_password(interaction: discord.Interaction, length: int):
    password = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k=length))
    embed = discord.Embed(title=f"{interaction.guild.name}", description=f"Your Generated Password: `{password}`", color=0x2b2d31)
    embed.set_footer(text=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
    await interaction.response.send_message(embed=embed, ephemeral=True)  

# Verbindung zur Datenbank herstellen
conn = sqlite3.connect('warn.db')
c = conn.cursor()

# Tabellen in der Datenbank erstellen
c.execute('''CREATE TABLE IF NOT EXISTS warns
             (user_id integer, reason text, num_warns integer)''')

# Warn-Command definieren
@bot.tree.command(description="Warn a Member")
async def warn(interaction: discord.Interaction, member: discord.Member, *, reason: str):
    # User-ID, Grund und Anzahl der Warnungen in die Datenbank schreiben
    c.execute("SELECT num_warns FROM warns WHERE user_id=?", (member.id,))
    num_warns = c.fetchone()
    if num_warns is None:
        c.execute("INSERT INTO warns VALUES (?, ?, ?)", (member.id, reason, 1))
        embed = discord.Embed(title=f"{interaction.guild.name}", description=f'{member.mention} wurde verwarnt für: `{reason}`. Das ist die erste Warnung.')
        embed.set_footer(text=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        embed = discord.Embed(title=f"{interaction.guild.name}", description=f'DU wurdest verwarnt für: `{reason}`. Das ist deine erste Warnung.')
        embed.set_footer(text=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
        await member.send(embed=embed)
    else:
        num_warns = num_warns[0] + 1
        c.execute("UPDATE warns SET reason=?, num_warns=? WHERE user_id=?", (reason, num_warns, member.id))
        embed = discord.Embed(title=f"{interaction.guild.name}", description=f'{member.mention} wurde verwarnt für: `{reason}`. Das ist die `{num_warns}`. Warnung.')
        embed.set_footer(text=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        embed = discord.Embed(title=f"{interaction.guild.name}", description=f'Du wurdest verwarnt für: `{reason}`. Das ist deine `{num_warns}`. Warnung.')
        embed.set_footer(text=f"{interaction.guild.name}", icon_url=f"{interaction.guild.icon}")
        await member.send(embed=embed)

        # Wenn der Benutzer drei oder mehr Warnungen hat, wird er gekickt
        if num_warns >= 3:
            await member.kick(reason=f'Zu viele Warnungen ({num_warns})')

    # Änderungen in der Datenbank speichern
    conn.commit()

# Initialisiere das Datenbank-Verbindungs-Objekt
conn = sqlite3.connect('level_system.db')

# Erstelle die Datenbank-Tabelle für die Benutzer-Level-Daten
conn.execute('''CREATE TABLE IF NOT EXISTS user_levels
             (user_id INTEGER PRIMARY KEY,
             xp INTEGER DEFAULT 0,
             level INTEGER DEFAULT 1)''')

# Funktion zur Aktualisierung der XP-Daten des Benutzers
def update_user_xp(user_id, xp):
    conn.execute("UPDATE user_levels SET xp = xp + ? WHERE user_id = ?", (xp, user_id,))
    conn.commit()

# Funktion zur Aktualisierung des Levels des Benutzers
def update_user_level(user_id):
    user_data = get_user_level_data(user_id)
    if user_data is None:
        conn.execute("INSERT INTO user_levels (user_id, level, xp) VALUES (?, 1, 0)", (user_id,))
        conn.commit()
    else:
        xp = user_data[1] + 5
        level = get_user_level_data(xp)
        conn.execute("UPDATE user_levels SET xp = ?, level = ? WHERE user_id = ?", (xp, level, user_id))
        conn.commit()

    xp = conn.execute("SELECT xp FROM user_levels WHERE user_id = ?", (user_id,)).fetchone()[0]
    level = int(((xp // 50) ** 0.5) + 1)
    conn.execute("UPDATE user_levels SET level = ? WHERE user_id = ?", (level, user_id,))
    conn.commit()

# Funktion zur Aktualisierung des Sprach-Levels des Benutzers
def update_user_voice_level(user_id):
    minutes = conn.execute("SELECT voice_minutes FROM user_levels WHERE user_id = ?", (user_id,)).fetchone()[0]
    voice_level = int(((minutes // 10) ** 0.5) + 1)
    conn.execute("UPDATE user_levels SET voice_level = ? WHERE user_id = ?", (voice_level, user_id,))
    conn.commit()

# Funktion zur Abfrage des Benutzer-Levels
def get_user_level(xp):
    return int((xp / 100) ** 0.5)

# Funktion zur Abfrage der Benutzer-Level-Daten
def get_user_level_data(user_id):
    data = conn.execute("SELECT level, xp FROM user_levels WHERE user_id = ?", (user_id,)).fetchone()
    if data is None:
        return None
    return data

# Discord.py Event zur Behandlung von Nachrichten
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    # Erhöhe die XP des Benutzers um 5 für jede Nachricht
    update_user_xp(message.author.id, 5)
    # Aktualisiere das Level des Benutzers
    old_level = get_user_level_data(message.author.id)
    update_user_level(message.author.id)
    new_level = get_user_level_data(message.author.id)
    if new_level[0] > old_level[0]:
        channel = bot.get_channel(850409719113842769)  # Gib hier die ID des Kanals ein, in dem die Nachricht gepostet werden soll
        embed = discord.Embed(title="Level Up!", description=f"Herzlichen Glückwunsch {message.author.mention}, du bist jetzt **Level {new_level[0]}** 🎉\n\nDu hast insgesamt **{new_level[1]//5}** Nachrichten geschrieben.", color=0x2b2d31)
        embed.set_thumbnail(url=f"{message.author.display_avatar}")
        embed.set_footer(text=f"{message.guild.name}", icon_url=f"{message.guild.icon}")
        await channel.send(embed=embed)
    await bot.process_commands(message)

# Discord.py Command zum Abrufen der Level-Daten eines Benutzers
@bot.command()
async def rank(ctx):
    user_data = get_user_level_data(ctx.author.id)
    level = user_data[0]
    xp = user_data[1]
    rank = conn.execute("SELECT COUNT() FROM user_levels WHERE xp > ?", (xp,)).fetchone()[0] + 1
    embed = discord.Embed(title=f"Rang von {ctx.author.name}", color=0x2b2d31)
    embed.set_thumbnail(url=ctx.author.display_avatar)
    embed.add_field(name="📈 Level", value=f"```{level}```", inline=True)
    embed.add_field(name="📊 Nachrichten", value=f"```{xp//5}```", inline=True)
    embed.add_field(name="👻 XP", value=f"```{xp}```", inline=True)
    embed.add_field(name="🥇 Server-Rang", value=f"```{rank} / {str(ctx.guild.member_count)}```", inline=False)
    embed.set_footer(text=f"{ctx.guild.name}", icon_url=f"{ctx.guild.icon}")
    await ctx.send(embed=embed)
    
bot.run(token)