import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from myserver import server_on

load_dotenv()


CHANNEL_ID = os.getenv('CHANNEL_ID')
ADMIN_ROLE = os.getenv('ADMIN_ROLE')
OWNER_ROLE = os.getenv('OWNER_ROLE')


CHANNEL_ID = int(CHANNEL_ID)
ADMIN_ROLE = int(ADMIN_ROLE)
OWNER_ROLE = int(OWNER_ROLE)


TOKEN = os.getenv('DISCORD_TOKEN')

if not TOKEN or not CHANNEL_ID or not ADMIN_ROLE or not OWNER_ROLE:
    print("Error: TOKEN, CHANNEL_ID, ADMIN_ROLE, or OWNER_ROLE is not set in .env")
    exit(1)


intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
intents.members = True

# หัวข้อคำสั่ง
bot = commands.Bot(command_prefix='/', intents=intents)

# เเจ้งบอทออนไลน์
@bot.event
async def on_ready():
    print('Moxz online🔥')
    try:
        channel = bot.get_channel(int(CHANNEL_ID))
        if channel:
            await channel.send("Moxz Online🔥")
            print(f"Successfully connected to channel: {CHANNEL_ID}")
            await bot.tree.sync()
            print("Slash commands synced!")
    except Exception as e:
        print(f"Error: {e}")



# /hello
@bot.tree.command(name='hello', description='ทักทายบอท')
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'สวัสดี {interaction.user.mention} ขอให้เป็นวันที่ดีน้า')



# /ping
@bot.tree.command(name='ping', description='เช็คการตอบสนองของบอท')
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000) 
    await interaction.response.send_message(f'Pong! ความหน่วง: {latency}ms')



# /info
@bot.tree.command(name='info', description='แสดงข้อมูลผู้ใช้หรือเซิร์ฟเวอร์')
async def info(interaction: discord.Interaction, target: discord.Member = None):
    if target is None:

        # แสดงข้อมูลเซิร์ฟเวอร์
        guild = interaction.guild
        embed = discord.Embed(title=f"Server Info: {guild.name}", color=0xffffff)
        embed.add_field(name="Server Name", value=guild.name, inline=False)
        embed.add_field(name="Server ID", value=guild.id, inline=False)
        embed.add_field(name="Member Count", value=guild.member_count, inline=False)
        await interaction.response.send_message(embed=embed)
    else:

        # แสดงข้อมูลผู้ใช้
        user = target
        embed = discord.Embed(title=f"User Info: {user.name}", color=0xff0000)
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.add_field(name="Username", value=user.name, inline=False)
        embed.add_field(name="User ID", value=user.id, inline=False)
        embed.add_field(name="Joined At", value=user.joined_at, inline=False)
        await interaction.response.send_message(embed=embed)



# /commands โชว์คำสั่งทั้งหมด
@bot.tree.command(name='commands', description='แสดงคำสั่งทั้งหมด')
async def show_commands(interaction: discord.Interaction):
    commands_list = ""
    for command in bot.tree.get_commands():
        commands_list += f"/{command.name}: {command.description}\n"
    
    await interaction.response.send_message(f"คำสั่งทั้งหมด:\n{commands_list}")



# /ban ผู้ใช้ Role Admin เท่านั้น
@bot.tree.command(name='ban', description='แบนผู้ใช้')
@commands.has_role(ADMIN_ROLE)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    if interaction.channel_id == int(CHANNEL_ID):
        if interaction.user.guild_permissions.ban_members:
            await member.ban(reason=reason)
            await interaction.response.send_message(f'{member.mention} ถูกแบนเรียบร้อยแล้ว เหตุผล: {reason}')
        else:
            await interaction.response.send_message('คุณไม่มีสิทธิ์แบนผู้ใช้', ephemeral=True)
    else:
        await interaction.response.send_message('คุณไม่สามารถใช้คำสั่งนี้ในช่องนี้ได้', ephemeral=True)

# /clear ลบคำ
@bot.tree.command(name='clear', description='ลบข้อความจำนวนที่ระบุ')
@commands.has_role(ADMIN_ROLE)
async def clear(interaction: discord.Interaction, amount: int):
    if interaction.channel_id == int(CHANNEL_ID):
        if interaction.user.guild_permissions.manage_messages:
            if amount <= 0:
                await interaction.response.send_message('จำนวนข้อความต้องมากกว่า 0', ephemeral=True)
                return
            elif amount > 100:
                await interaction.response.send_message('คุณสามารถลบได้สูงสุด 100 ข้อความในคราวเดียว', ephemeral=True)
                return

            await interaction.response.defer(ephemeral=True)
            
            channel = interaction.channel
            deleted = await channel.purge(limit=amount)

            await interaction.followup.send(f'ลบข้อความ {len(deleted)} ข้อความเรียบร้อยแล้ว', ephemeral=True)
        else:
            await interaction.response.send_message('คุณไม่มีสิทธิ์จัดการข้อความ', ephemeral=True)
    else:
        await interaction.response.send_message('คุณไม่สามารถใช้คำสั่งนี้ในช่องนี้ได้', ephemeral=True)



# /shutdown ปิดบอทเฉราะเจ้าของ 
@bot.tree.command(name='shutdown', description='ปิดบอท (เฉพาะเจ้าของ)')
async def shutdown(interaction: discord.Interaction):
    try:
        owner_role_id = int(OWNER_ROLE)
        if any(role.id == owner_role_id for role in interaction.user.roles):
            await interaction.response.send_message("Moxz Offline💀...")
            await bot.close()
        else:
            await interaction.response.send_message("คุณไม่มีสิทธิ์ใช้คำสั่งนี้", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"เกิดข้อผิดพลาด: {str(e)}")

server_on()

bot.run(TOKEN)