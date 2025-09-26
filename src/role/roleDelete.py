import discord
import logging

logger = logging.getLogger('discord')

async def delete_role(ctx, role_name: str):
    role_name = role_name.strip()
    if not role_name:
        await ctx.send("Usage: !delete role RoleName")
        return

    guild = ctx.guild
    role = discord.utils.find(lambda r: r.name.lower() == role_name.lower(), guild.roles)
    if not role:
        await ctx.send(f'Role "{role_name}" not found.')
        return

    try:
        await role.delete(reason="Role deleted via bot command")
        await ctx.send(f'Role "{role_name}" deleted successfully.')
        logger.info(f'Role "{role_name}" deleted by {ctx.author}')
    except discord.Forbidden:
        await ctx.send("I don't have permission to delete roles.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
