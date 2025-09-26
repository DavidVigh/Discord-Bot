import discord

async def create_role(ctx, role_name: str, color: str = "#ffffff"):
    guild = ctx.guild
    existing_role = discord.utils.get(guild.roles, name=role_name)
    if existing_role:
        await ctx.send(f'Role "{role_name}" already exists.')
        return
    try:
        color_value = int(color[1:], 16) if color.startswith("#") else int(color, 16)
        discord_color = discord.Color(color_value)
        new_role = await guild.create_role(name=role_name, color=discord_color)
        await ctx.send(f'Role "{new_role.name}" created successfully with color {color}!')
    except ValueError:
        await ctx.send("Invalid color format. Use hex code like #ff0000.")
    except discord.Forbidden:
        await ctx.send("I don't have permission to create roles.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
