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
from src.permissionController import permission_controller

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
async def delete(ctx, *, type_: str):
    await delete_controller(ctx, type_)

# ASSIGN COMMAND
@bot.command(name="assign")
@commands.has_permissions(manage_roles=True)
async def assign(ctx, *, args):
    """
    Usage:
    !assign role RoleName -c CategoryName
    !assign @user RoleName
    """
    args_list = args.split()
    if len(args_list) >= 2 and args_list[0].lower() == "role" and "-c" in args_list:
        role_index = 1
        c_index = args_list.index("-c")
        role_name = " ".join(args_list[role_index:c_index])
        category_name = " ".join(args_list[c_index+1:])
        await assign_controller(ctx, role_name=role_name, category_name=category_name)
        return

    # Handle member assignment
    if ctx.message.mentions:
        member = ctx.message.mentions[0]
        role_name = " ".join(args_list[1:])
        await assign_controller(ctx, member=member, role_name=role_name)
        return

    await ctx.send("Invalid command format. Use `!assign role RoleName -c CategoryName` or `!assign @user RoleName`")

# REVOKE COMMAND
@bot.command(name="revoke")
@commands.has_permissions(manage_roles=True)
async def revoke(ctx, *, args):
    """
    Usage:
    !revoke role RoleName -c CategoryName
    !revoke @user RoleName
    """
    args_list = args.split()
    if len(args_list) >= 2 and args_list[0].lower() == "role" and "-c" in args_list:
        role_index = 1
        c_index = args_list.index("-c")
        role_name = " ".join(args_list[role_index:c_index])
        category_name = " ".join(args_list[c_index+1:])
        await revoke_controller(ctx, role_name=role_name, category_name=category_name)
        return

    # Handle member revocation
    if ctx.message.mentions:
        member = ctx.message.mentions[0]
        role_name = " ".join(args_list[1:])
        await revoke_controller(ctx, member=member, role_name=role_name)
        return

    await ctx.send("Invalid command format. Use `!revoke role RoleName -c CategoryName` or `!revoke @user RoleName`")

# PERM COMMAND

@bot.command(name="perm")
@commands.has_permissions(manage_roles=True, manage_channels=True)
async def perm(ctx, *, command_text: str):
    """
    Usage:
    !perm RoleName CategoryName add|remove perm1,perm2
    !perm RoleName CategoryName set default|moderator|admin
    """
    parts = command_text.split()

    # Find the action index
    try:
        action_index = next(i for i, part in enumerate(parts) if part.lower() in ["add", "remove", "set"])
    except StopIteration:
        await ctx.send("Missing action: 'add', 'remove' or 'set'.")
        return

    action = parts[action_index]
    permissions = " ".join(parts[action_index + 1:])
    before_action = parts[:action_index]

    if len(before_action) < 2:
        await ctx.send("Please provide both role name and category name.")
        return

    role_name = before_action[0]
    category_name = " ".join(before_action[1:])

    await permission_controller(ctx, role_name, category_name, action, permissions=permissions)

# Run the bot
bot.run(token, log_handler=handler, log_level=logging.DEBUG)