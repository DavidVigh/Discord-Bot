import discord
import logging

logger = logging.getLogger('discord')


async def revoke_role_from_category(guild: discord.Guild, role_name: str, category_name: str):
    """
    Revoke a role from a category by removing its access to all channels under that category.
    Specifically denies view_channel so the role cannot see channels.
    """
    role = discord.utils.find(lambda r: r.name.lower() == role_name.lower(), guild.roles)
    if not role:
        raise ValueError(f'Role "{role_name}" not found.')

    category = discord.utils.find(lambda c: c.name.lower() == category_name.lower(), guild.categories)
    if not category:
        raise ValueError(f'Category "{category_name}" not found.')

    # Deny all relevant permissions (especially view_channel)
    overwrite = discord.PermissionOverwrite()
    overwrite.view_channel = False
    overwrite.send_messages = False
    overwrite.connect = False
    overwrite.speak = False

    for channel in category.channels:
        await channel.set_permissions(role, overwrite=overwrite)

    logger.info(f'Role "{role_name}" revoked from category "{category_name}". View denied for all channels.')
    return category.name
