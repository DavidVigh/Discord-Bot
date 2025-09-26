import discord

from .role.roleRevoke import revoke_role

async def revoke_controller(ctx, member: discord.Member = None, *, role_name: str = None):
    await revoke_role(ctx, member=member, role_name=role_name)