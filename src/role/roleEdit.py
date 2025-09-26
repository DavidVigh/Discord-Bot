import discord

async def edit_role(ctx, role_name: str, what_to_edit: str, new_value: str = None):
    guild = ctx.guild
    role = discord.utils.get(guild.roles, name=role_name)
    if not role:
        await ctx.send(f'Role "{role_name}" not found.')
        return
    kwargs = {}

    # Map short permission names to full ones
    perm_aliases = {
        "kick": "kick_members",
        "ban": "ban_members",
        "manage": "manage_messages",
        "admin": "administrator",
        "mention": "mentionable",
        "hoist": "hoist",
        "manage_roles": "manage_roles",
        "manage_channels": "manage_channels",
        "read": "read_messages",
        "send": "send_messages",
        "embed": "embed_links",
        "attach": "attach_files",
        "voice": "connect",
        "speak": "speak",
        "mute": "mute_members",
        "deafen": "deafen_members",
        "move": "move_members",
        "priority": "priority_speaker"
    }

    try:
        permission_triggers = ["permission", "permissions", "-p"]
        name_triggers = ["name", "-n"]
        color_triggers = ["color", "-c"]

        # Color editing: if what_to_edit is a color trigger or a hex code
        if (
            what_to_edit.lower() in color_triggers and new_value
        ) or (
            what_to_edit.startswith("#")
        ):
            # Accept either !edit "role name" color #hex OR !edit "role name" #hex
            hex_code = new_value if what_to_edit.lower() in color_triggers else what_to_edit
            if hex_code and hex_code.startswith("#") and len(hex_code) == 7:
                try:
                    color_value = int(hex_code[1:], 16)
                    kwargs["color"] = discord.Color(color_value)
                    await role.edit(**kwargs, reason="Role color edited via bot command")
                    await ctx.send(f'Role color updated to "{hex_code}".')
                    return
                except ValueError:
                    await ctx.send("Invalid color format. Use hex code like #ff0000.")
                    return
            else:
                await ctx.send("Please provide a valid hex color code (e.g. #ff0000).")
                return

        # Permission editing
        if what_to_edit.lower() in permission_triggers and new_value:
            perm_names = [p.strip() for p in new_value.split(",")]
            perms = role.permissions
            toggled = []
            invalid_perms = []
            for name in perm_names:
                perm_name = perm_aliases.get(name, name)
                if hasattr(perms, perm_name):
                    current = getattr(perms, perm_name)
                    setattr(perms, perm_name, not current)
                    toggled.append(f"{perm_name}: {not current}")
                else:
                    invalid_perms.append(name)
            if toggled:
                kwargs["permissions"] = perms
            if invalid_perms:
                await ctx.send(f"Invalid permission(s): {', '.join(invalid_perms)}")
                return
            if toggled:
                await role.edit(**kwargs, reason="Role edited via bot command")
                await ctx.send(f'Role "{role_name}" updated:\n' + "\n".join(toggled))
                return

        # Name editing
        elif what_to_edit.lower() in name_triggers and new_value:
            kwargs["name"] = new_value
            await role.edit(**kwargs, reason="Role name edited via bot command")
            await ctx.send(f'Role name updated to "{new_value}".')
            return

        else:
            await ctx.send('Use `help` or `-h` for help.')
            return

    except ValueError:
        await ctx.send("Invalid value format.")
    except discord.Forbidden:
        await ctx.send("I don't have permission to edit roles.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
