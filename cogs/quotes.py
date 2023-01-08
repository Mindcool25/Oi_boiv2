from random import choice
import re
import discord
from discord.ext import commands

import json

# Quotes cog class
class Quotes(commands.Cog):

    # Letting the cog connect to bot
    def __init__(self, bot):
        self.bot = bot

    # Get random quote from json file
    @discord.slash_command()
    async def quote(self, ctx, word = ""):
        msg = await ctx.respond("Searching...")

        # Opening and parsing json file
        # This is done here to allow hotloading stuff
        f = open("cogs/quotes.json")
        quotes = json.load(f)
        f.close()

        # Getting a random quote, either from search or from everything
        if word == "":
            # Grabbing a random quote
            quote, author = choice(list(quotes.items()))
            # Formatting quote
            send = f"{quote}\n- {author}"
        else:
            # Get all quotes with specified word
            found_quotes = []
            for i in quotes:
                if word in i:
                    found_quotes.append([i, quotes[i]])
                elif word in quotes[i]:
                    found_quotes.append([i, quotes[i]])
            print(found_quotes)
            quote, author = choice(found_quotes)

            send = f"{quote}\n- {author}"

        # Sending chosen quote
        print(f"Sending quote:\n{send}")
        print(ctx.author)
        await msg.edit_original_response(content=send)

    # Collecting quotes from channel command was executed in
    @discord.slash_command()
    async def collect(self, ctx):
        channel = ctx.channel
        col = ""
        async for i in channel.history():
            if i.content != "":
                print(i.content)
                col += i.content + "\n"
        # AHHH scary regex
        found = re.findall("(\(.*\))*(\*.*\*)*.*(.*(\"|“|”).*(\"|“|”).*(\(.*\))*(\*.*\*)*( )*\n*)+(-.*)+", col)

        # Parsing result from regex
        parsed = {}
        for quote in found:
            out = ""
            # I'm sorry for the magic numbers here, but it is needed.
            out = f"{quote[0]}{quote[1]}{quote[2]}{quote[5]}{quote[6]}{quote[7]}".strip("\n")
            author = quote[8]
            parsed[out] = author
        print("Parsed quotes:", parsed)

        # Add to json file after looking for duplicates
        await ctx.respond(f"Found and parsed {len(found)} quotes. Adding to database.")

        add_to_database(parsed)
        


# Adds cog to bot when called
def setup(bot):
    bot.add_cog(Quotes(bot))

def add_to_database(parsed_quotes):
    # Grab current quotes
    f = open("cogs/quotes.json")
    quotes = json.load(f)
    f.close()

    # Check for duplicates, otherwise add quote.
    for key in parsed_quotes.keys():
        if key in quotes.keys():
            print("Duplicate found. Ignoring.")
        else:
            print(f"Adding '{key}' to quotes")
            quotes[key] = parsed_quotes[key]
    json_obj = json.dumps(quotes, indent=2)
    
    with open("cogs/out.json", "w") as outfile:
        outfile.write(json_obj)

