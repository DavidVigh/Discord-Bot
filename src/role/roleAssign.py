import discord

async def assign_role(ctx, member: discord.Member = None, *, role_name: str = None):
    # If member is not provided, try to get from mentions
    if member is None and ctx.message.mentions:
        member = ctx.message.mentions[0]
    if member is None or role_name is None:
        await ctx.send('Usage: !assign @user role_name')
        return

    guild = ctx.guild
    role = discord.utils.get(guild.roles, name=role_name)
    if not role:
        await ctx.send(f'Role "{role_name}" not found.')
        return
    try:
        await member.add_roles(role, reason="Role assigned via bot command")
        await ctx.send(f'Role "{role_name}" assigned to {member.mention}.')
    except discord.Forbidden:
        await ctx.send("I don't have permission to assign roles.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")