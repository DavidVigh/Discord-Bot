import discord

from .role.roleAssign import assign_role

async def assign_controller(ctx, member: discord.Member = None, *, role_name: str = None):
    await assign_role(ctx, member=member, role_name=role_name)