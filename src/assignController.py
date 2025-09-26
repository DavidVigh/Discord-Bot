import discord
from .category.categoryAssign import assign_role_to_category

async def assign_controller(ctx, member: discord.Member = None, role_name: str = None, *, category_name: str = None):
    """
    Assign a role or member to a category.
    """
    guild = ctx.guild

    if role_name and category_name:
        try:
            category_assigned = await assign_role_to_category(guild, role_name, category_name)
            await ctx.send(f'Role "{role_name}" can now access all channels in category "{category_assigned}".')
        except ValueError as e:
            await ctx.send(str(e))
        except discord.Forbidden:
            await ctx.send("I don't have permission to assign roles to this category.")
        return

    if member and role_name:
        role = discord.utils.get(guild.roles, name=role_name)
        if not role:
            await ctx.send(f'Role "{role_name}" not found.')
            return
        try:
            await member.add_roles(role, reason="Role assigned via bot command")
            await ctx.send(f'Role "{role_name}" assigned to {member.mention}.')
        except discord.Forbidden:
            await ctx.send("I don't have permission to assign roles.")
        return

    await ctx.send("Usage: !assign role RoleName -c CategoryName OR !assign @user RoleName")
