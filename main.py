import discord
import dotenv
import os

# Setting up env variables (Hey look, actually protecting my token)
dotenv.load_dotenv()
token = str(os.getenv("TOKEN"))

# Setting up the bot object
bot = discord.Bot()

# Onready function
@bot.event
async def on_ready():
    print(f"{bot.user} is loaded.")

# Basically hello world
@bot.slash_command(name="ping", description = "Pong!")
async def ping(ctx):
    await ctx.respond("Pong!")

# Loading cogs
extensions = ["cogs.quotes"]

for cog in extensions:
    bot.load_extension(cog)
    print(f"Loaded cog: {cog}")


bot.run(token)
