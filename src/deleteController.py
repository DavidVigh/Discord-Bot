import discord
from .role.roleDelete import delete_role

async def delete_controller(ctx, *, role_name: str = None):
    await delete_role(ctx, role_name=role_name)