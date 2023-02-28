import discord
import os
import asyncio
from keep_alive import keep_alive

bot = discord.Bot()
bot.author_id = 576372354670919690

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.slash_command()
async def helloji(ctx):
    await ctx.respond("Hello!")

extensions = [
    'cogs.cog_manager',
    'cogs.ask_opportunity_commands',
    'cogs.post_opportunity_commands',
    'cogs.query_opportunities'
  
]

token = os.environ.get('discord_bot_key')
def main():
      for extension in extensions:
         bot.load_extension(extension)
      print(f'Cogs loaded: {", ".join(bot.cogs)}')
      bot.run(token)
  
keep_alive()
main()
