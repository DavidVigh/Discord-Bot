import discord

async def delete_role(ctx, *, role_name: str = None):
    if role_name is None:
        await ctx.send('Usage: !delete role_name')
        return

    guild = ctx.guild
    role = discord.utils.get(guild.roles, name=role_name)
    if not role:
        await ctx.send(f'Role "{role_name}" not found.')
        return
    try:
        await role.delete(reason="Role deleted via bot command")
        await ctx.send(f'Role "{role_name}" deleted successfully.')
    except discord.Forbidden:
        await ctx.send("I don't have permission to delete roles.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")