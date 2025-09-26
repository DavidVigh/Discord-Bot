import discord

async def create_channel(ctx, channel_type: str, channel_name: str, category_name: str = None):
    guild = ctx.guild
    category = None
    if category_name:
        category = discord.utils.get(guild.categories, name=category_name)
    try:
        if channel_type == "text":
            new_channel = await guild.create_text_channel(channel_name, category=category)
        elif channel_type == "voice":
            new_channel = await guild.create_voice_channel(channel_name, category=category)
        else:
            await ctx.send('Invalid channel type. Use "text" or "voice".')
            return
        await ctx.send(f'{channel_type.capitalize()} channel "{new_channel.name}" created successfully!')
    except discord.Forbidden:
        await ctx.send(f"I don't have permission to create {channel_type} channels.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")