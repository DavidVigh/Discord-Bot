import discord
from src.role.roleEdit import edit_role
import logging

logger = logging.getLogger('discord')

async def edit_controller(ctx, role_name: str, what_to_edit: str, new_value: str = None):
    await edit_role(ctx, role_name=role_name, what_to_edit=what_to_edit, new_value=new_value)

