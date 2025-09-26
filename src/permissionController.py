import discord
import logging

logger = logging.getLogger('discord')


# Predefined permission sets
PERMISSION_SHORTCUTS = {
    "default": ["view_channel", "send_messages", "connect", "speak"],
    "moderator": ["view_channel", "send_messages", "connect", "speak", "manage_messages", "timeout_members"],
    "admin": ["view_channel", "send_messages", "connect", "speak", "manage_messages",
              "timeout_members", "manage_channels", "manage_roles", "administrator"]
}


async def set_category_permissions(category: discord.CategoryChannel, role_name: str, action: str, permissions: str, guild: discord.Guild):
    """
    Set permissions for a role on a category.
    """
    role = discord.utils.find(lambda r: r.name.lower() == role_name.lower(), guild.roles)
    if not role:
        raise ValueError(f'Role "{role_name}" not found.')

    changed = []

    # Handle 'set' action with shortcuts
    if action.lower() == "set":
        shortcut = permissions.strip().lower()
        if shortcut not in PERMISSION_SHORTCUTS:
            raise ValueError(f'Unknown shortcut "{shortcut}". Use: default, moderator, admin.')

        perms_list = PERMISSION_SHORTCUTS[shortcut]
    else:
        perms_list = [p.strip().lower() for p in permissions.split(",") if p.strip()]
        if not perms_list:
            raise ValueError("No permissions specified.")

    # Permission aliases (for add/remove)
    perm_aliases = {
        "view": "view_channel",
        "send": "send_messages",
        "connect": "connect",
        "speak": "speak",
        "embed": "embed_links",
        "attach": "attach_files",
        "manage": "manage_channels",
        "kick": "kick_members",
        "ban": "ban_members",
        "mute": "mute_members",
        "deafen": "deafen_members",
        "move": "move_members",
        "manage_messages": "manage_messages",
        "timeout_members": "timeout_members",
        "administrator": "administrator",
        "manage_roles": "manage_roles"
    }

    overwrite = category.overwrites_for(role)

    for perm in perms_list:
        perm_name = perm_aliases.get(perm, perm)
        if not hasattr(overwrite, perm_name):
            continue

        if action.lower() == "add":
            setattr(overwrite, perm_name, True)
        elif action.lower() == "remove":
            setattr(overwrite, perm_name, False)
        elif action.lower() == "set":
            setattr(overwrite, perm_name, True)

        changed.append(f"{perm_name}: {getattr(overwrite, perm_name)}")

    await category.set_permissions(role, overwrite=overwrite)
    logger.info(f'Permissions for role "{role_name}" updated on category "{category.name}": {changed}')
    return changed


async def permission_controller(ctx, role_name: str, category_name: str, action: str, *, permissions: str):
    """
    Controller for category permissions
    """
    guild = ctx.guild
    category = discord.utils.find(lambda c: c.name.lower() == category_name.lower(), guild.categories)
    if not category:
        await ctx.send(f'Category "{category_name}" not found.')
        return

    try:
        changed = await set_category_permissions(category, role_name, action, permissions, guild)
        if changed:
            await ctx.send(f'Permissions updated for category "{category_name}" on role "{role_name}":\n' + "\n".join(changed))
        else:
            await ctx.send("No valid permissions were modified.")
    except ValueError as e:
        await ctx.send(str(e))
    except discord.Forbidden:
        await ctx.send("I don't have permission to edit this category.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
