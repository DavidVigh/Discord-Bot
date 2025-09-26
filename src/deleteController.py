import discord
from src.role.roleDelete import delete_role
from src.category.categoryDelete import delete_category
from src.channel.channelDelete import delete_channel
import logging

logger = logging.getLogger('discord')

async def delete_controller(ctx, type_: str):
    """
    Controller for !delete command.
    Syntax:
      !delete role RoleName
      !delete category CategoryName
      !delete channel ChannelName [-category CategoryName]
    """
    parts = type_.split(maxsplit=1)
    if len(parts) < 2:
        await ctx.send('Usage: !delete <role|category|channel> <name> [optional category]')
        return

    entity_type, name = parts[0].lower(), parts[1]

    try:
        if entity_type == "role":
            await delete_role(ctx, name)
        elif entity_type == "category":
            await delete_category(ctx, name)
        elif entity_type == "channel":
            await delete_channel(ctx, name)
        else:
            await ctx.send('Invalid type. Use: role, category, or channel.')
            return
        logger.info(f'{entity_type} deletion requested by {ctx.author}: {name}')
    except discord.Forbidden:
        await ctx.send(f"I don't have permission to delete {entity_type}.")
    except Exception as e:
        await ctx.send(f"An error occurred while deleting {entity_type}: {e}")