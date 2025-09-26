import discord
from src.role.roleCreate import create_role
from src.category.categoryCreate import create_category
from src.channel.channelCreate import create_channel

async def create_controller(ctx, type_: str, *args):
    """
    Controller for the !create command.
    Supports:
      - Roles: !create role RoleName [#hexcolor]
      - Categories: !create category CategoryName
      - Channels: !create text/voice ChannelName [category/-c CategoryName]
    """
    type_lower = type_.lower()

    if type_lower == "role":
        if len(args) == 0:
            await ctx.send('Usage: !create role RoleName [#hexcolor]')
            return
        # Handle multi-word role names + optional color
        if len(args) >= 2 and args[-1].startswith("#"):
            color = args[-1]
            role_name = " ".join(args[:-1])
        else:
            color = "#ffffff"
            role_name = " ".join(args)
        await create_role(ctx, role_name, color)

    elif type_lower == "category":
        if len(args) == 0:
            await ctx.send('Usage: !create category CategoryName')
            return
        category_name = " ".join(args)
        await create_category(ctx, category_name)

    elif type_lower in ["text", "voice"]:
        if len(args) == 0:
            await ctx.send(f'Usage: !create {type_lower} ChannelName [category/-c CategoryName]')
            return
        await create_channel(ctx, type_lower, *args)

    else:
        await ctx.send('Invalid type. Use: role, category, text, or voice.')