from discord.ext import commands
import discord


class DevCommands(commands.Cog, name='Developer Commands'):
  '''These are the developer commands'''

  def __init__(self, bot):
    self.bot = bot

  async def cog_check(self, ctx: discord.ApplicationContext):
    '''
		The default check for this cog whenever a command is used. Returns True if the command is allowed.
		'''
    return ctx.author.id == self.bot.author_id

  @commands.slash_command(name='reload', description='reloads a cog')
  async def reload(self, ctx: discord.ApplicationContext, cog):
    '''Reloads a cog.'''

    extensions = self.bot.extensions
    if cog == 'all':  #reload all cogs at once
      for extension in extensions:
        self.bot.unload_extension(f'cogs.{cog}')
        self.bot.load_extension(f'cogs.{cog}')
      await ctx.respond('Done')
    print(self.bot.extensions)
    if f'cogs.{cog}' in extensions:
      self.bot.unload_extension(f'cogs.{cog}')  # Unloads the cog
      self.bot.load_extension(f'cogs.{cog}')  # Loads the cog
      await ctx.respond(f'Reloaded {cog}')
    else:
      await ctx.respond('Unknown Cog')

  @commands.slash_command(name="unload")
  async def unload(self, ctx: discord.ApplicationContext, cog):
    '''Unload a cog.'''

    extensions = self.bot.extensions
    if f'cogs.{cog}' not in extensions:
      await ctx.respond("Cog is not loaded!")
      return
    self.bot.unload_extension(f'cogs.{cog}')
    await ctx.respond(f"`{cog}` has successfully been unloaded.")

  @commands.slash_command(name="load")
  async def load(self, ctx: discord.ApplicationContext, cog):
    '''Loads a cog.'''

    try:
      self.bot.load_extension(f'cogs.{cog}')
      await ctx.respond(f"`{cog}` has successfully been loaded.")
    except commands.errors.ExtensionNotFound:
      await ctx.respond(f"`{cog}` does not exist!")

  @commands.slash_command(name="listcogs")
  async def listcogs(self, ctx: discord.ApplicationContext):
    '''Returns a list of all enabled commands.'''

    base_string = "```css\n"
    base_string += "\n".join([str(cog) for cog in self.bot.extensions])
    base_string += "\n```"

    await ctx.respond(base_string)


def setup(bot):
  bot.add_cog(DevCommands(bot))
