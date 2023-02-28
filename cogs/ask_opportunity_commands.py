import discord
from discord.ui import InputText, View, Modal
from discord.ext import commands
from json_edit import edit_datajson, get_datajson
from vals import OPPORTUNITY_ASKING_CHANNEL_ID
import datetime


class MakeOpportunityMessage():

  def __init__(self, bot: discord.Bot):
    self.bot = bot

  async def make_message(self):
    channel = self.bot.get_channel(
      OPPORTUNITY_ASKING_CHANNEL_ID)  #opportunity channel id
    data = get_datajson("opportunity_data")
    author_id = data["added_by"]
    author_mention = f"<@{author_id}>"
    author_info = await self.bot.fetch_user(author_id)
    about = data["about"]
    description = data["description"]
    lookingfor = data["looking_for"]

    embed = discord.Embed(title=about,
                          description=description,
                          color=discord.Colour.blurple(),
                          timestamp=datetime.datetime.utcnow())
    embed.set_author(name=author_info)
    embed.set_footer(text="by sphinx bot")
    embed.set_thumbnail(url=author_info.avatar)
    embed.add_field(name="Looking for : ", value=lookingfor)
    embed.set_image(
      url=
      'https://cdn.discordapp.com/attachments/560753089179680768/594957849797460177/Epic_gif-1.gif'
    )

    a = await channel.send(embed=embed)
    await a.add_reaction(emoji="✨")
    thread = await a.create_thread(name=about)
    edit_datajson("opportunity_data", "thread_link", thread.jump_url)
    await thread.send(author_mention)


class AskOpportunity(Modal):

  def __init__(self, title, bot: discord.Bot, ctx: discord.ApplicationContext):
    super().__init__(title=title)
    self.ctx = ctx
    self.bot = bot
    self.add_item(
      InputText(
        label='Short intro',
        required=True,
        max_length=100,
        custom_id='about',
        style=discord.InputTextStyle.short,
      ))
    self.add_item(
      InputText(
        label='What are you looking for?',
        required=True,
        max_length=100,
        custom_id='looking_for',
        style=discord.InputTextStyle.long,
      ))
    self.add_item(
      InputText(
        label='Write something more about yourself',
        placeholder='About...',
        required=True,
        max_length=1000,
        custom_id='description',
        style=discord.InputTextStyle.long,
      ))

  async def callback(self, interaction: discord.Interaction):
    await interaction.response.defer()
    edit_datajson("opportunity_data", "about", self.children[0].value)
    edit_datajson("opportunity_data", "looking_for", self.children[1].value)
    edit_datajson("opportunity_data", "description", self.children[2].value)

    m = MakeOpportunityMessage(self.bot)
    await m.make_message()


class OpportunityCommands(commands.Cog):

  def __init__(self, bot):
    super().__init__()
    self.bot = bot

  @commands.slash_command(description='Ask for opportunities')
  async def ask_opportunity(self, ctx: discord.ApplicationContext):
    a = AskOpportunity('Ask for opprtunity', self.bot, ctx)
    await ctx.send_modal(a)
    edit_datajson("opportunity_data", "added_by", ctx.author.id)


def setup(bot):
  bot.add_cog(OpportunityCommands(bot))
