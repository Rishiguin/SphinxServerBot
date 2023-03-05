import discord
import os
import asyncio
from keep_alive import keep_alive
from discord.ext import commands

bot = discord.Bot(command_prefix='%',help_command=commands.DefaultHelpCommand())
bot.author_id = 576372354670919690

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.slash_command(description = "See the different commands")
async def help(ctx):
    await ctx.respond("`/seek_opportunity` : introduce and ask for opportunities\n\n`/add_opportunity` : add a job or opportunity\n\n`/search_opportunity` : search for opportunities\n\n `/event_create` : create an event")

@bot.event
async def on_message(ctx):
  if ctx.channel.id == 1069614589114855526: #welcome channel id
    await ctx.add_reaction("👋")
    await ctx.create_thread(name=f"Hi there {ctx.author}, welcome to Indian Tech Discord")

extensions = [
    'cogs.cog_manager',
    'cogs.ask_opportunity_commands',
    'cogs.post_opportunity_commands',
    'cogs.query_opportunities',
    'cogs.event_commands'
  
]

token = os.environ.get('discord_bot_key')
def main():
      for extension in extensions:
         bot.load_extension(extension)
      print(f'Cogs loaded: {", ".join(bot.cogs)}')
      bot.run(token)
  
keep_alive()
main()
