import discord
import logging

logger = logging.getLogger('discord')

async def delete_channel(ctx, args: str):
    """
    Delete a text or voice channel with optional category.
    
    Syntax:
        !delete channel Channel Name [-category Category Name]
        !delete channel Channel Name [category Category Name]
        !delete channel Channel Name         # no category
    """
    if not args:
        await ctx.send('Usage: !delete channel <Channel Name> [-category <Category Name>]')
        return

    args_lower = args.lower()

    # Parse for category flag
    if "-category" in args_lower:
        parts = args_lower.split("-category", maxsplit=1)
        channel_name = parts[0].strip()
        category_name = parts[1].strip()
    elif "category" in args_lower:
        parts = args_lower.split("category", maxsplit=1)
        channel_name = parts[0].strip()
        category_name = parts[1].strip()
    else:
        channel_name = args.strip()
        category_name = None

    if not channel_name:
        await ctx.send('Usage: !delete channel <Channel Name> [-category <Category Name>]')
        return

    guild = ctx.guild
    channel = None

    # Find category if specified
    category = None
    if category_name:
        category = discord.utils.find(lambda c: c.name.lower() == category_name.lower(), guild.categories)
        if not category:
            await ctx.send(f'Category "{category_name}" not found.')
            return
        # Find channel inside this category
        channel = discord.utils.find(lambda ch: ch.name.lower() == channel_name.lower() and ch.category == category, guild.channels)
    else:
        # Find channel with no category
        channel = discord.utils.find(lambda ch: ch.name.lower() == channel_name.lower() and ch.category is None, guild.channels)

    if not channel:
        await ctx.send(f'Channel "{channel_name}" not found in the specified scope.')
        return

    try:
        await channel.delete(reason="Channel deleted via bot command")
        await ctx.send(f'Channel "{channel_name}" deleted successfully!')
        logger.info(f'Channel "{channel_name}" deleted by {ctx.author}')
    except discord.Forbidden:
        await ctx.send("I don't have permission to delete this channel.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
