import discord
from discord.ui import InputText, View, Modal, Select
from discord.ext import commands
from json_edit import edit_datajson, get_datajson
from vals import OPPORTUNITY_ASKING_CHANNEL_ID, ROLES, TOPICS
import datetime
from sqlite_functions import get_jobs


class SendQueryResult():

  def __init__(self, bot: discord.Bot, ctx: discord.ApplicationContext):
    self.bot = bot
    self.ctx = ctx
    self.data = get_datajson("query_data")
    self.type_tag = self.data["type_tags"][0]
    self.compensation_tags = self.data["compensation_tags"]
    print('compensation tags : ', self.compensation_tags)
    print('type_tag ',self.type_tag)

  async def make_message(self):
    
    q = "type = '{}' AND compensation IN {}".format(
      self.type_tag, tuple(self.compensation_tags) if len(self.compensation_tags)>1 else f'("{self.compensation_tags[0]}")')
    print(q)
    results = get_jobs(q)
    
    if results != 400 and results is not None:
      description = ''
      for result in results:
        about = result[0]
        compensation = result[1]
        link = result[2]
        description += f"`{compensation}`\n[{about}]({link})\n\n"
    else:
      description = 'No opportunities found'
    print(description)
    embed = discord.Embed(
      title=self.type_tag,
      description=description,
      color=discord.Colour.blurple(),
    )
    embed.set_footer(text="by sphinx bot")
    embed.set_image(
      url=
      'https://cdn.discordapp.com/attachments/560753089179680768/594957849797460177/Epic_gif-1.gif'
    )

    await self.ctx.send(embed=embed)


class JobTypeDropdown(Select):

  def __init__(self, bot: discord.Bot):
    self.bot = bot
    roles = ROLES.keys()
    options = []
    for role in roles:
      options.append(discord.SelectOption(label=role))

    super().__init__(
      placeholder="Type",
      min_values=1,
      max_values=1,
      options=options,
    )

  async def callback(self, interaction: discord.Interaction):
    await interaction.response.defer()
    edit_datajson("query_data", "type_tags", tuple(self.values))


class CompensationDropdown(Select):

  def __init__(self, bot_: discord.Bot, ctx: discord.ApplicationContext):
    self.bot = bot_
    self.ctx = ctx

    options = [
      discord.SelectOption(label=l) for l in TOPICS
    ]  #the name TOPICS is quite confusing, have to change to monetary or compensation or something else

    super().__init__(
      placeholder="$$$ (multiple can be selected)",
      min_values=1,
      max_values=4,
      options=options,
    )

  async def callback(self, interaction: discord.Interaction):
    await interaction.response.send_message('Searching...', ephemeral=True)
    edit_datajson("query_data", "compensation_tags",
                  tuple(self.values))  #tuple because python can't hash list

    query = SendQueryResult(self.bot, self.ctx)
    await query.make_message()


class DropdownViewQueryJobs(discord.ui.View):

  def __init__(self, bot_: discord.Bot, ctx: discord.ApplicationContext):
    self.ctx = ctx
    self.bot = bot_
    super().__init__()

    # Adds the dropdown to our View object
    self.add_item(JobTypeDropdown(self.bot))
    self.add_item(CompensationDropdown(self.bot, self.ctx))


class QueryCommands(commands.Cog):

  def __init__(self, bot):
    super().__init__()
    self.bot = bot

  @commands.slash_command(description='Ask for opportunities')
  async def search_opportunity(self, ctx: discord.ApplicationContext):
    a = DropdownViewQueryJobs(self.bot, ctx)
    await ctx.respond(view=a)


def setup(bot):
  bot.add_cog(QueryCommands(bot))
