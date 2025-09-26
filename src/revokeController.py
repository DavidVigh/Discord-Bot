import discord
from .category.categoryRevoke import revoke_role_from_category

async def revoke_controller(ctx, member: discord.Member = None, role_name: str = None, *, category_name: str = None):
    guild = ctx.guild

    if role_name and category_name:
        try:
            category_revoked = await revoke_role_from_category(guild, role_name, category_name)
            await ctx.send(f'Role "{role_name}" no longer has access to category "{category_revoked}".')
        except ValueError as e:
            await ctx.send(str(e))
        except discord.Forbidden:
            await ctx.send("I don't have permission to revoke roles from this category.")
        return

    if member and role_name:
        role = discord.utils.get(guild.roles, name=role_name)
        if not role:
            await ctx.send(f'Role "{role_name}" not found.')
            return
        try:
            await member.remove_roles(role, reason="Role removed via bot command")
            await ctx.send(f'Role "{role_name}" removed from {member.mention}.')
        except discord.Forbidden:
            await ctx.send("I don't have permission to remove roles.")
        return

    await ctx.send("Usage: !revoke role RoleName -c CategoryName OR !revoke @user RoleName")
