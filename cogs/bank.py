import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta
import sqlite3

color = 0x2b2d31

conn = sqlite3.connect('bank.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS accounts (user_id text, bank_balance INTEGER, cash_balance INTEGER, last_beggars datetime)''')
c.execute('''CREATE TABLE IF NOT EXISTS items (name text, price INTEGER)''')
c.execute('''CREATE TABLE IF NOT EXISTS inventory (user_id text, item_name text, quantity INTEGER)''')

class Bank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description="Erstelle ein Account bei der Bank")
    async def create_account(self, interactions: discord.Interaction):
        c.execute("SELECT * FROM accounts WHERE user_id=?", (interactions.user.id,))
        account = c.fetchone()
        if account is not None:
            embed = discord.Embed(title=f"{interactions.guild.name}", description="Du hast bereits ein Konto.", color=color)
            embed.set_footer(text=f"{interactions.guild.name}", icon_url=f"{interactions.guild.icon}")
            await interactions.response.send_message(embed=embed, ephemeral=True)
            return
        
        c.execute("INSERT INTO accounts VALUES (?, ?, ?, ?)", (interactions.user.id, 0, 0, None))
        conn.commit()
        embed = discord.Embed(title=f"{interactions.guild.name}", description="Dein Konto wurde erfolgreich erstellt.", color=color)
        embed.set_footer(text=f"{interactions.guild.name}", icon_url=f"{interactions.guild.icon}")
        await interactions.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(description="Löscht den Account eines Benutzers")
    async def reset_account(self, interactions: discord.Interaction, user: discord.Member):
        c.execute("DELETE FROM accounts WHERE user_id=?", (user.id,)) # Löscht den User von der Datenbank
        c.execute("DELETE FROM inventory WHERE user_id=?", (user.id,)) # Enfernt das Inventar des Users
        conn.commit()

        embed = discord.Embed(title=f"{interactions.guild.name}", description=f"Der Account von {user.mention} wurde zurückgesetzt.", color=color)
        embed.set_footer(text=f"{interactions.guild.name}", icon_url=f"{interactions.guild.icon}")
        await interactions.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(description="Nach Geld betteln")
    async def beg(self, interactions: discord.Interaction):
        c.execute("SELECT * FROM accounts WHERE user_id=?", (interactions.user.id,))
        account = c.fetchone()
        if account is None:
            embed = discord.Embed(title=f"{interactions.guild.name}", description=f"Du hast noch kein Konto. Bitte erstelle zuerst ein Konto mit dem Command `/create_account`.", color=color)
            embed.set_footer(text=f"{interactions.guild.name}", icon_url=f"{interactions.guild.icon}")
            await interactions.response.send_message(embed=embed, ephemeral=True)
            return
        
        last_beggars = account[3]
        if last_beggars is not None and datetime.now() - datetime.strptime(last_beggars, "%Y-%m-%d %H:%M:%S.%f") < timedelta(hours=1):
            embed = discord.Embed(title=f"{interactions.guild.name}", description=f"{interactions.user.mention} Du kannst nur einmal pro Stunde betteln.", color=color)
            embed.set_footer(text=f"{interactions.guild.name}", icon_url=f"{interactions.guild.icon}")
            await interactions.response.send_message(embed=embed, ephemeral=True)
            return
        
        amount = 50
        cash_balance = account[2] + amount
        c.execute("UPDATE accounts SET cash_balance=?, last_beggars=? WHERE user_id=?", (cash_balance, datetime.now(), interactions.user.id))
        conn.commit()
        embed = discord.Embed(title=f"{interactions.guild.name}", description=f"Du hast `{amount} Coins` in Bar erhalten.", color=color)
        embed.set_footer(text=f"{interactions.guild.name}", icon_url=f"{interactions.guild.icon}")
        await interactions.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(description="Sehe dein Kontostand")
    async def balance(self, interactions: discord.Interaction):
        c.execute("SELECT * FROM accounts WHERE user_id=?", (interactions.user.id,))
        account = c.fetchone()
        if account is None:
            embed = discord.Embed(title=f"{interactions.guild.name}", description=f"Du hast noch kein Konto. Bitte erstelle zuerst ein Konto mit dem Command `/create_account`.", color=color)
            embed.set_footer(text=f"{interactions.guild.name}", icon_url=f"{interactions.guild.icon}")
            await interactions.response.send_message(embed=embed, ephemeral=True)
            return
        
        bank_balance = account[1]
        cash_balance = account[2]
        embed = discord.Embed(title=f"{interactions.user.name} Balance", color=color)
        embed.set_thumbnail(url=f"{interactions.user.display_avatar}")
        embed.add_field(name="Bank", value=f"{bank_balance} Coins")
        embed.add_field(name="Cash", value=f"{cash_balance} Coins")
        embed.set_footer(text=f"{interactions.guild.name}", icon_url=f"{interactions.guild.icon}")
        await interactions.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(description="Geld auf Bankkonto einzahlen")
    async def deposit(self, interactions: discord.Interaction, amount: int):
        c.execute("SELECT * FROM accounts WHERE user_id=?", (interactions.user.id,))
        account = c.fetchone()
        if account is None:
            embed = discord.Embed(title=f"{interactions.guild.name}", description=f"Du hast noch kein Konto. Bitte erstelle zuerst ein Konto mit dem Command `/create_account`.", color=color)
            embed.set_footer(text=f"{interactions.guild.name}", icon_url=f"{interactions.guild.icon}")
            await interactions.response.send_message(embed=embed, ephemeral=True)
            return
        
        if account[2] < amount:
            embed = discord.Embed(title=f"{interactions.guild.name}", description="Du hast nicht genug Bargeld.", color=color)
            embed.set_footer(text=f"{interactions.guild.name}", icon_url=f"{interactions.guild.icon}")
            await interactions.response.send_message(embed=embed, ephemeral=True)
            return
        
        cash_balance = account[2] - amount
        bank_balance = account[1] + amount
        c.execute("UPDATE accounts SET cash_balance=?, bank_balance=? WHERE user_id=?", (cash_balance, bank_balance, interactions.user.id))
        conn.commit()
        
        embed = discord.Embed(title=f"{interactions.guild.name}", description=f"Es wurden {amount} Coins Bargeld auf dein Bankkonto eingezahlt.", color=color)
        embed.set_footer(text=f"{interactions.guild.name}", icon_url=f"{interactions.guild.icon}")
        await interactions.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(description="Geld vom bankkonto abheben")
    async def withdraw(self, interactions: discord.Interaction, amount: int):
        c.execute("SELECT * FROM accounts WHERE user_id=?", (interactions.user.id,))
        account = c.fetchone()
        if account is None:
            embed = discord.Embed(title=f"{interactions.guild.name}", description=f"Du hast noch kein Konto. Bitte erstelle zuerst ein Konto mit dem Command `/create_account`.", color=color)
            embed.set_footer(text=f"{interactions.guild.name}", icon_url=f"{interactions.guild.icon}")
            await interactions.response.send_message(embed=embed, ephemeral=True)
            return
        
        if account[1] < amount:
            embed = discord.Embed(title=f"{interactions.guild.name}", description="Du hast nicht genug Geld auf deinem Bankkonto.", color=color)
            embed.set_footer(text=f"{interactions.guild.name}", icon_url=f"{interactions.guild.icon}")
            await interactions.response.send_message(embed=embed, ephemeral=True)
            return
        
        bank_balance = account[1] - amount
        cash_balance = account[2] + amount
        c.execute("UPDATE accounts SET bank_balance=?, cash_balance=? WHERE user_id=?", (bank_balance, cash_balance, interactions.user.id))
        conn.commit()
        
        embed = discord.Embed(title=f"{interactions.guild.name}", description=f"Du hast {amount} Coins von deinem Bankkonto abgehoben.", color=color)
        embed.set_footer(text=f"{interactions.guild.name}", icon_url=f"{interactions.guild.icon}")
        await interactions.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(description="Einem anderen Spieler Geld überweisen")
    async def transfer(self, interactions: discord.Interaction, member: discord.Member, amount: int):
        c.execute("SELECT * FROM accounts WHERE user_id=?", (interactions.user.id,))
        sender_account = c.fetchone()
        if sender_account is None:
            embed = discord.Embed(title=f"{interactions.guild.name}", description=f"Du hast noch kein Konto. Bitte erstelle zuerst ein Konto mit dem Command `/create_account`.", color=color)
            embed.set_footer(text=f"{interactions.guild.name}", icon_url=f"{interactions.guild.icon}")
            await interactions.response.send_message(embed=embed, ephemeral=True)
            return
        
        if sender_account[2] < amount:
            embed = discord.Embed(title=f"{interactions.guild.name}", description="Du hast nicht genug Geld.", color=color)
            embed.set_footer(text=f"{interactions.guild.name}", icon_url=f"{interactions.guild.icon}")
            await interactions.response.send_message(embed=embed, ephemeral=True)
            return
        
        c.execute("SELECT * FROM accounts WHERE user_id=?", (member.id,))
        member_account = c.fetchone()
        if member_account is None:
            embed = discord.Embed(title=f"{interactions.guild.name}", description=f"{member.mention} hat noch kein Konto.", color=color)
            embed.set_footer(text=f"{interactions.guild.name}", icon_url=f"{interactions.guild.icon}")
            await interactions.response.send_message(embed=embed, ephemeral=True)
            return
        
        sender_balance = sender_account[2] - amount
        member_balance = member_account[2] + amount
        c.execute("UPDATE accounts SET cash_balance=? WHERE user_id=?", (sender_balance, interactions.user.id))
        c.execute("UPDATE accounts SET cash_balance=? WHERE user_id=?", (member_balance, member.id))
        conn.commit()
        
        embed = discord.Embed(title=f"{interactions.guild.name}", description=f"Du hast {member.mention} {amount} Coins überwiesen.", color=color)
        embed.set_footer(text=f"{interactions.guild.name}", icon_url=f"{interactions.guild.icon}")
        await interactions.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(description="Einem Member Geld überweisen")
    async def addmoney(self, interactions: discord.Interaction, user:discord.Member, amount: int):
        c.execute("SELECT * FROM accounts WHERE user_id=?", (user.id,))
        recipient_account = c.fetchone()
        if recipient_account is None:
            embed = discord.Embed(title=f"{interactions.guild.name}", description=f"{user} besitzt leider kein Konto bei der Bank.", color=color)
            embed.set_footer(text=f"{interactions.guild.name}", icon_url=f"{interactions.guild.icon}")
            await interactions.response.send_message(embed=embed, ephemeral=True)
            return

        recipient_balance = recipient_account[2] + amount
        c.execute("UPDATE accounts SET cash_balance=? WHERE user_id=?", (recipient_balance, user.id))
        conn.commit()

        embed = discord.Embed(title=f"{interactions.guild.name}", description=f"**{user.mention} hat nun `{amount}` Coins erhalten.**", color=color)
        embed.set_footer(text=f"{interactions.guild.name}", icon_url=f"{interactions.guild.icon}")
        await interactions.response.send_message(embed=embed, ephemeral=True)    

    @app_commands.command(description="Zeigt unseren Shop an")
    async def shop(self, interactions: discord.Interaction):
        c.execute("SELECT name, price FROM items")
        items = c.fetchall()

        embed = discord.Embed(title="Shop", color=color)
        embed.set_author(name=f"{interactions.guild.name}", icon_url=f"{interactions.guild.icon}")
        embed.set_thumbnail(url=f"{interactions.guild.icon}")
        for item in items:
            embed.add_field(name=item[0], value=f"**Preis:** `{item[1]} Coins`", inline=False)
        embed.set_footer(text=f"{interactions.guild.name}", icon_url=f"{interactions.guild.icon}")
        await interactions.response.send_message(embed=embed)

    @app_commands.command(description="Füge ein Item hinzu")
    async def add_item(self, interactions: discord.Interaction, item_name: str, item_price: int):
        c.execute("INSERT INTO items (name, price) VALUES (?, ?)", (item_name, item_price))
        conn.commit()
        embed = discord.Embed(title=f"{interactions.guild.name}", description=f"{item_name} wurde zum Shop hinzugefügt.", color=color)
        embed.set_footer(text=f"{interactions.guild.name}", icon_url=f"{interactions.guild.icon}")
        await interactions.response.send_message(embed=embed, ephemeral=True)
        member = interactions.guild.get_member(interactions.user.id)

    @app_commands.command(description="Entferne ein Item")
    async def remove_item(self, interactions: discord.Interaction, item_name: str):
        c.execute("DELETE FROM items WHERE name=?", (item_name,))
        conn.commit()
        embed = discord.Embed(title=f"{interactions.guild.name}", description=f"{item_name} wurde aus dem Shop entfernt.", color=color)
        embed.set_footer(text=f"{interactions.guild.name}", icon_url=f"{interactions.guild.icon}")
        await interactions.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(description="Kauf ein Item aus dem Shop")
    async def buy(self, interactions: discord.Interaction, item_name: str):
        c.execute("SELECT price FROM items WHERE name=?", (item_name,))
        item_price = c.fetchone()

        if item_price is None:
            embed = discord.Embed(title=f"{interactions.guild.name}", description="Dieses Item ist nicht im Shop vorhanden.", color=color)
            embed.set_footer(text=f"{interactions.guild.name}", icon_url=f"{interactions.guild.icon}")
            await interactions.response.send_message(embed=embed, ephemeral=True)
            return

        c.execute("SELECT bank_balance FROM accounts WHERE user_id=?", (interactions.user.id,))
        user_balance = c.fetchone()

        if user_balance is None:
            embed = discord.Embed(title=f"{interactions.guild.name}", description="Du hast kein Bank-Konto. Bitte erstelle eines mit `/create_account`.", color=color)
            embed.set_footer(text=f"{interactions.guild.name}", icon_url=f"{interactions.guild.icon}")
            await interactions.response.send_message(embed=embed, ephemeral=True)
            return

        bank_balance = user_balance[0]
        if bank_balance < item_price[0]:
            embed = discord.Embed(title=f"{interactions.guild.name}", description="Du hast nicht genug Geld.", color=color)
            embed.set_footer(text=f"{interactions.guild.name}", icon_url=f"{interactions.guild.icon}")
            await interactions.response.send_message(embed=embed, ephemeral=True)
            return

        new_bank_balance = bank_balance - item_price[0]
        c.execute("UPDATE accounts SET bank_balance=? WHERE user_id=?", (new_bank_balance, interactions.user.id))

        c.execute("INSERT INTO inventory (user_id, item_name) VALUES (?, ?)", (interactions.user.id, item_name))

        conn.commit()

        embed = discord.Embed(title=f"{interactions.guild.name}", description=f"Du hast dir `{item_name}` gekauft.\nDein neuer Bank-Kontostand beträgt `{new_bank_balance}` Coins.", color=color)
        embed.set_footer(text=f"{interactions.guild.name}", icon_url=f"{interactions.guild.icon}")
        await interactions.response.send_message(embed=embed, ephemeral=True)
        member = interactions.guild.get_member(interactions.user.id)
        role = discord.utils.get(interactions.guild.roles, name="YourRoleNameHere")
        await member.add_roles(role)

        channel = self.bot.get_channel(1084488342655205466)
        embed = discord.Embed(title=f"{interactions.user}", description="Ein Kunde hat etwas im Shop gekauft", color=color)
        embed.set_thumbnail(url=f"{interactions.user.display_avatar}")
        embed.add_field(name="Kunde", value=f"{interactions.user.mention}", inline=True)
        embed.add_field(name="Ware", value=f"`{item_name}`", inline=True)
        embed.set_footer(text=f"{interactions.guild.name}", icon_url=f"{interactions.guild.icon}")
        await channel.send(embed=embed)

    @app_commands.command(description="Item zurückgeben")
    async def rebuy(self, interactions: discord.Interaction, item_name: str):
        c.execute("SELECT price FROM items WHERE name=?", (item_name,))
        item_price = c.fetchone()

        if item_price is None:
            embed = discord.Embed(title=f"{interactions.guild.name}", description="Dieses Item existiert nicht oder du hast es nicht gekauft.", color=color)
            embed.set_footer(text=f"{interactions.guild.name}", icon_url=f"{interactions.guild.icon}")
            await interactions.response.send_message(embed=embed, ephemeral=True)
            return

        c.execute("SELECT bank_balance FROM accounts WHERE user_id=?", (interactions.user.id,))
        user_balance = c.fetchone()

        if user_balance is None:
            embed = discord.Embed(title=f"{interactions.guild.name}", description="Du hast kein Bank-Konto. Bitte erstelle eines mit `/create_account`.", color=color)
            embed.set_footer(text=f"{interactions.guild.name}", icon_url=f"{interactions.guild.icon}")
            await interactions.response.send_message(embed=embed, ephemeral=True)
            return

        bank_balance = user_balance[0]
        new_bank_balance = bank_balance + item_price[0]
        c.execute("UPDATE accounts SET bank_balance=? WHERE user_id=?", (new_bank_balance, interactions.user.id))

        c.execute("DELETE FROM inventory WHERE user_id=? AND item_name=?", (interactions.user.id, item_name))
        conn.commit()

        embed = discord.Embed(title=f"{interactions.guild.name}", description=f"{item_name} wurde zurückerstattet.\nDein neuer Bank-Kontostand beträgt `{new_bank_balance}` Coins.", color=color)
        embed.set_footer(text=f"{interactions.guild.name}", icon_url=f"{interactions.guild.icon}")
        await interactions.response.send_message(embed=embed, ephemeral=True)
        member = interactions.guild.get_member(interactions.user.id)
        role = discord.utils.get(interactions.guild.roles, name="YourRoleNameHere")
        await member.remove_roles(role)

async def setup(bot):
    await bot.add_cog(Bank(bot))
    print("cogs.bank")
