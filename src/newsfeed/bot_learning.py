import discord
from discord.ext import commands

# Define the bot's intents
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True  # Enable message content intent

# Define the bot with the specified intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Event handler for when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print('------')

# Command to send a message
@bot.command()
async def send_message(ctx):
    # Replace 'your_channel_id' with the actual channel ID where you want to send the message
    channel = bot.get_channel(1148542025491288095)
    
    # Send a message to the specified channel
    await channel.send('Hello World')
    print('Command executed: !send_message')

@bot.command()
async def shutdown(ctx):
    if ctx.author.id == 222845856540393482:  # Replace YOUR_USER_ID with your Discord user ID
        await ctx.send("Shutting down the bot. Goodbye!")
        await bot.logout()
    else:
        await ctx.send("You don't have permission to shut down the bot.")

# Run the bot with your bot token
bot.run('MTE0ODUyNTIzOTU1MTE0ODEwNQ.GkzZlp.B5-nUyWAEAX0ZW8F0C0v4_LL9JT_QaXDPRMKAQ')
