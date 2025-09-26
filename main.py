import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import requests

from src.createController import create_controller
from src.editController import edit_controller
from src.deleteController import delete_controller

from src.assignController import assign_controller
from src.revokeController import revoke_controller

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user.name}')

# Event: Member joins the server
@bot.event
async def member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name='join')
    if channel:
        await channel.send(f'Welcome to the server, {member.mention}!')
    

# Censorship setup (VIA api Ninjas)
censor_api_key = os.getenv('CENSOR_API_KEY')

""" @bot.event

async def on_message(message):
    if message.author == bot.user:
        return

    api_url = "https://api.api-ninjas.com/v1/profanityfilter"
    headers = {
        "X-Api-Key": censor_api_key
    }
    params = {
        "text": message.content
    }
    response = requests.get(api_url, headers=headers, params=params)
    if response.status_code == 200:
        censored = response.json().get("censored", "")
        if censored and censored != message.content:
            await message.delete()
            await message.channel.send(f'{message.author.mention} - your message was censored:\n{censored}')

    await bot.process_commands(message)

async def create_role_helper(ctx, role_name: str, color: str = "#ffffff"):
    guild = ctx.guild
    existing_role = discord.utils.get(guild.roles, name=role_name)
    if existing_role:
        await ctx.send(f'Role "{role_name}" already exists.')
        return
    try:
        color_value = int(color[1:], 16) if color.startswith("#") else int(color, 16)
        discord_color = discord.Color(color_value)
        new_role = await guild.create_role(name=role_name, color=discord_color)
        await ctx.send(f'Role "{new_role.name}" created successfully with color {color}!')
    except ValueError:
        await ctx.send("Invalid color format. Use hex code like #ff0000.")
    except discord.Forbidden:
        await ctx.send("I don't have permission to create roles.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
 """
# ...existing code...

# CREATE COMMAND
@bot.command(name="create")
@commands.has_permissions(manage_roles=True, manage_channels=True)
async def create(ctx, type_: str, *args):
    await create_controller(ctx, type_, *args)

# EDIT COMMAND
@bot.command(name="edit")
@commands.has_permissions(manage_roles=True)
async def edit(ctx, role_name: str, what_to_edit: str, new_value: str = None):
    await edit_controller(ctx, role_name, what_to_edit, new_value)

# DELETE COMMAND
@bot.command(name="delete")
@commands.has_permissions(manage_roles=True)
async def delete_role(ctx, *, role_name: str = None):
    await delete_controller(ctx, role_name=role_name)

# ASSIGN COMMAND
@bot.command(name="assign")
@commands.has_permissions(manage_roles=True)
async def assign(ctx, member: discord.Member = None, *, role_name: str = None):
    await assign_controller(ctx, member=member, role_name=role_name)

# REVOKE COMMAND
@bot.command(name="revoke")
@commands.has_permissions(manage_roles=True)
async def revoke(ctx, member: discord.Member = None, *, role_name: str = None):
    await revoke_controller(ctx, member=member, role_name=role_name)


# Run the bot
bot.run(token, log_handler=handler, log_level=logging.DEBUG)