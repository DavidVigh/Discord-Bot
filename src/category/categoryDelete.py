import discord

async def delete_category(ctx, category_name: str):
    guild = ctx.guild
    category = discord.utils.get(guild.categories, name=category_name)
    if not category:
        await ctx.send(f'Category "{category_name}" does not exist.')
        return
    try:
        await category.delete()
        await ctx.send(f'Category "{category_name}" has been deleted successfully.')
    except discord.Forbidden:
        await ctx.send("I don't have permission to delete categories.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")