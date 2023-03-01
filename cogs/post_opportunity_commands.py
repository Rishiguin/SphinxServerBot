import discord
from discord.ui import Button, InputText, View, Modal, Select
from discord.ext import commands
from discord import Embed, Interaction, ActionRow, SelectMenu, SelectOption, Message
import ui_components
from discord.ext.commands import Context
from json_edit import edit_datajson, get_datajson
from vals import ROLES, TOPICS, JOB_CHANNEL_ID
import asyncio
from sqlite_functions import add_job
import datetime


class MakeJobMessage():

  def __init__(self, bot: discord.Bot):
    self.bot = bot
    self.data = get_datajson('job_data')
    self.author_id = self.data["added_by"]
    self.author_mention = f"<@{self.author_id}>"
    self.about = self.data["about"]
    self.description = self.data["description"]
    self.type = self.data["type_tags"][0]
    self.compensation = self.data["topic_tags"][0]
    self.role_id = ROLES[self.type]["role_id"]
    self.role_mention = "<@&{}>".format(self.role_id)
    print(self.role_id)
    self.channel = self.bot.get_channel(JOB_CHANNEL_ID)
    self.lookingfor=self.data["looking_for"].strip().split(',')

  def add_to_database(self, thread_url):
    add_job(type=self.type,
            author_id=self.author_id,
            about=self.about,
            description=self.description,
            compensation=self.compensation,
            thread_link=thread_url)

  async def make_message(self):
    author_info = await self.bot.fetch_user(self.author_id)
    embed = discord.Embed(title=self.about,
                          description=self.description + '\n',
                          color=discord.Colour.green(),
                          timestamp=datetime.datetime.utcnow())
    lookingfor_msg='' 
    for quality in self.lookingfor:
      lookingfor_msg+=f'`{quality.strip()}`\n '
      
    embed.set_footer(text="via pyramid")
    embed.add_field(name="Looking for people who are :",value=lookingfor_msg)
    embed.add_field(name="Added by:", value=self.author_mention,inline=False)
    embed.add_field(name="Type:", value=self.role_mention)
    embed.add_field(name="$$$:", value=self.compensation)

    a = await self.channel.send(embed=embed)
    await a.add_reaction(emoji="👋")
    thread = await a.create_thread(name=self.about)
    await thread.send(self.author_mention)
    await thread.send(self.role_mention)

    edit_datajson("job_data", "thread_link", thread.jump_url)
    self.add_to_database(str(thread.jump_url))


class AddJob(Modal):

  def __init__(self, title, bot: discord.Bot, ctx: discord.ApplicationContext):
    super().__init__(title=title)
    self.ctx = ctx
    self.bot = bot
    self.add_item(
      InputText(
        label='Opportunity title and short intro',
        placeholder="Frontend engineer at Sphinx.co",
        required=True,
        max_length=80,
        custom_id='about',
        style=discord.InputTextStyle.short,
      ))
    self.add_item(
      InputText(
        label='Description about the opportunity',
        required=True,
        max_length=1000,
        custom_id='description',
        style=discord.InputTextStyle.long,
      ))
    self.add_item(
      InputText(
        label='Skills/Qualities you are looking for',
        placeholder=
        '(comma separated list)e.g:\nhardworking, enthusiastic about learning new things, strong in javascript',
        required=True,
        max_length=1000,
        custom_id='qualities_skills',
        style=discord.InputTextStyle.long,
      ))

  async def callback(self, interaction: discord.Interaction):
    v = DropdownViewPostJob(self.bot)
    await interaction.response.send_message(view=v)
    edit_datajson("job_data", "about", self.children[0].value)
    edit_datajson("job_data", "description", self.children[1].value)
    edit_datajson("job_data","looking_for",self.children[2].value)


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
    await interaction.response.send_message(f'{self.values}\n', ephemeral=True)
    edit_datajson("job_data", "type_tags",
                  tuple(self.values))  #tuple because python can't hash list


class TopicsDropdown(Select):

  def __init__(self, bot_: discord.Bot):
    self.bot = bot_

    options = [
      discord.SelectOption(label=l) for l in TOPICS
    ]  #the name TOPICS is quite confusing, have to change to monetary or compensation or something else

    super().__init__(
      placeholder="$$$",
      min_values=1,
      max_values=1,
      options=options,
    )

  async def callback(self, interaction: discord.Interaction):
    await interaction.response.send_message(f'{self.values}\n', ephemeral=True)
    edit_datajson("job_data", "topic_tags",
                  tuple(self.values))  #tuple because python can't hash list
    m = MakeJobMessage(self.bot)
    await m.make_message()


class DropdownViewPostJob(discord.ui.View):

  def __init__(self, bot_: discord.Bot):
    self.bot = bot_
    super().__init__()

    # Adds the dropdown to our View object
    self.add_item(JobTypeDropdown(self.bot))
    self.add_item(TopicsDropdown(self.bot))


class AddOpportunity(commands.Cog):

  def __init__(self, bot):
    super().__init__()
    self.bot = bot

  @commands.slash_command(description='Add a job/opportunity')
  async def add_opportunity(self, ctx: discord.ApplicationContext):
    a = AddJob(title='Submit job/opprtunity', bot=self.bot, ctx=ctx)
    await ctx.send_modal(a)
    edit_datajson("job_data", "added_by", ctx.author.id)


def setup(bot):
  bot.add_cog(AddOpportunity(bot))
