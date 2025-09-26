import discord
from src.role.roleCreate import create_role
from src.category.categoryCreate import create_category
from src.channel.channelCreate import create_channel

async def create_controller(ctx, type_: str, *args):
    if type_.lower() == "role":
        if len(args) == 0:
            await ctx.send('Usage: !create role role_name [#hexcolor]')
            return
        role_name = args[0]
        color = args[1] if len(args) > 1 else "#ffffff"
        await create_role(ctx, role_name, color)
    elif type_.lower() == "category":
        if len(args) == 0:
            await ctx.send('Usage: !create category category_name')
            return
        category_name = " ".join(args)
        await create_category(ctx, category_name)
    elif type_.lower() in ["text", "voice"]:
        if len(args) == 0:
            await ctx.send(f'Usage: !create {type_} channel_name [category_name]')
            return
        channel_name = args[0]
        category_name = " ".join(args[1:]) if len(args) > 1 else None
        await create_channel(ctx, type_.lower(), channel_name, category_name)
    else:
        await ctx.send('Invalid type. Use: role, category, text, or voice.')