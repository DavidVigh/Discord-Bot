import discord

async def create_category(ctx, category_name: str):
    guild = ctx.guild
    existing_category = discord.utils.get(guild.categories, name=category_name)
    if existing_category:
        await ctx.send(f'Category "{category_name}" already exists.')
        return
    try:
        new_category = await guild.create_category(category_name)
        await ctx.send(f'Category "{new_category.name}" created successfully!')
    except discord.Forbidden:
        await ctx.send("I don't have permission to create categories.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
