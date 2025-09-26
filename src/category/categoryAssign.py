import discord
import logging

logger = logging.getLogger('discord')


async def assign_role_to_category(guild: discord.Guild, role_name: str, category_name: str):
    """
    Assign a role to a category by granting basic permissions (view, send, connect, speak)
    for all channels under that category.
    """
    role = discord.utils.find(lambda r: r.name.lower() == role_name.lower(), guild.roles)
    if not role:
        raise ValueError(f'Role "{role_name}" not found.')

    category = discord.utils.find(lambda c: c.name.lower() == category_name.lower(), guild.categories)
    if not category:
        raise ValueError(f'Category "{category_name}" not found.')

    # Define the default permissions a role should have in this category
    overwrite = discord.PermissionOverwrite()
    overwrite.view_channel = True
    overwrite.send_messages = True
    overwrite.connect = True
    overwrite.speak = True

    # Apply overwrites to all channels in the category
    for channel in category.channels:
        await channel.set_permissions(role, overwrite=overwrite)

    logger.info(f'Role "{role_name}" assigned to category "{category_name}".')
    return category.name
