import discord
from discord.utils import get

# Predefined role permission sets
PERMISSION_SHORTCUTS = {
    "default": ["read_messages", "send_messages", "connect", "speak"],
    "moderator": ["read_messages", "send_messages", "connect", "speak",
                  "manage_messages", "timeout_members"],
    "admin": ["read_messages", "send_messages", "connect", "speak",
              "manage_messages", "timeout_members", "manage_channels",
              "manage_roles", "administrator"]
}


async def edit_role(ctx, role_name: str, what_to_edit: str, new_value: str = None):
    """
    Edit a role's properties: name, color, permissions, or shortcuts.
    """
    guild = ctx.guild
    role = get(guild.roles, name=role_name)
    if not role:
        await ctx.send(f'Role "{role_name}" not found.')
        return

    try:
        if what_to_edit.lower() == "set" and new_value:
            shortcut = new_value.lower()
            if shortcut not in PERMISSION_SHORTCUTS:
                await ctx.send(f'Unknown shortcut "{new_value}". Use: default, moderator, admin.')
                return

            perms_list = PERMISSION_SHORTCUTS[shortcut]
            perms = role.permissions
            # Reset all to False first
            for field in perms.__slots__:
                setattr(perms, field, False)
            # Apply shortcut permissions
            for perm in perms_list:
                if hasattr(perms, perm):
                    setattr(perms, perm, True)

            await role.edit(permissions=perms, reason=f'Role edited via shortcut "{shortcut}"')
            await ctx.send(f'Role "{role_name}" updated with shortcut "{shortcut}".')
            return

        # Existing color editing, name editing, or permission toggles...
        # Keep your previous implementation here if needed
        await ctx.send('Use `-h` or `help` for other editing commands.')

    except discord.Forbidden:
        await ctx.send("I don't have permission to edit this role.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
