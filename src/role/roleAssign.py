import discord
import logging

logger = logging.getLogger('discord')

async def assign_role(ctx, member: discord.Member, *, role_name: str):
    role_name = role_name.strip()
    guild = ctx.guild
    role = discord.utils.find(lambda r: r.name.lower() == role_name.lower(), guild.roles)
    if not role:
        await ctx.send(f'Role "{role_name}" not found.')
        return
    if role in member.roles:
        await ctx.send(f'{member.mention} already has the role "{role_name}".')
        return

    try:
        await member.add_roles(role, reason="Role assigned via bot command")
        await ctx.send(f'Role "{role_name}" assigned to {member.mention}.')
        logger.info(f'Role "{role_name}" assigned to {member} by {ctx.author}')
    except discord.Forbidden:
        await ctx.send("I don't have permission to assign roles.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
