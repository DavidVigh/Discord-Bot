import discord
import logging

logger = logging.getLogger('discord')

async def create_channel(ctx, channel_type: str, *args):
    """
    Create a text or voice channel with optional category.
    
    Syntax:
        !create text Channel Name category Category Name
        !create voice Channel Name -c Category Name
        !create text Channel Name          # no category
    """
    guild = ctx.guild
    category_name = None
    channel_name_parts = []

    # Parse args for category flag
    i = 0
    while i < len(args):
        arg = args[i].lower()
        if arg in ["category", "-c"] and i + 1 < len(args):
            # All remaining args belong to category name
            category_name = " ".join(args[i + 1:]).strip()
            break
        else:
            channel_name_parts.append(args[i])
        i += 1

    if not channel_name_parts:
        await ctx.send(f"Usage: !create {channel_type} <Channel Name> [category/-c <Category Name>]")
        return

    channel_name = "-".join(channel_name_parts).lower()[:100]  # Discord channel formatting

    # Find category if specified
    category = None
    if category_name:
        category = discord.utils.find(lambda c: c.name.lower() == category_name.lower(), guild.categories)
        if not category:
            await ctx.send(f'Category "{category_name}" not found.')
            return

    # Check if channel exists in the target category (or globally if no category)
    if category:
        existing_channel = discord.utils.find(lambda ch: ch.name.lower() == channel_name.lower() and ch.category == category, guild.channels)
    else:
        existing_channel = discord.utils.find(lambda ch: ch.name.lower() == channel_name.lower() and ch.category is None, guild.channels)

    if existing_channel:
        await ctx.send(f'A channel named "{channel_name}" already exists in the specified category.')
        return

    try:
        if channel_type.lower() == "text":
            new_channel = await guild.create_text_channel(channel_name, category=category)
        elif channel_type.lower() == "voice":
            new_channel = await guild.create_voice_channel(channel_name, category=category)
        else:
            await ctx.send('Invalid channel type. Use "text" or "voice".')
            return

        await ctx.send(f'{channel_type.capitalize()} channel "{new_channel.name}" created successfully!')
        logger.info(f'{channel_type.capitalize()} channel "{new_channel.name}" created by {ctx.author}')

    except discord.Forbidden:
        await ctx.send(f"I don’t have permission to create {channel_type} channels.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
