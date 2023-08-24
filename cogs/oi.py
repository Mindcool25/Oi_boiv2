import discord
from discord.ext import commands

# Oi cog class
class Oi(commands.Cog):
    # Connecting cog to bot
    def __init__(self, bot):
        self.bot = bot
        return

    @discord.slash_command()
    async def oi(self, ctx, number = ""):
        if number == "":
            number = 5
        else:
            try:
                number = int(number)
            except ValueError as error:
                await ctx.respond(f"{number} is not a number.")
                print(error)
                return
        for i in range(0, number):
            await ctx.respond("Oi")
        return

def setup(bot):
    bot.add_cog(Oi(bot))
