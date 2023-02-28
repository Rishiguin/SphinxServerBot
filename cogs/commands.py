import discord
from discord.ui import Button, InputText, View, Modal, Select
from discord.ext import commands
from discord import Embed, Interaction, ActionRow, SelectMenu, SelectOption, Message
import ui_components
from discord.ext.commands import Context
from json_edit import edit_datajson, get_datajson
from vals import ROLES, TOPICS, SKILLS
import asyncio

TEST_GUILD = discord.Object('731060009659662406')

# modals work
#buttons work
#dropdown callback work now

#⚠️⚠️⚠️⚠️ THIS IS OUT OF VERSION NOW, I SPARATED INTO INTO DIFFERENT COMMAND FILES


class MakeJobMessage():
  def __init__(self,bot: discord.Bot):
    self.bot=bot
    
  async def make_message(self):
    channel=self.bot.get_channel(1079525055844864183)
    data=get_datajson('job_data')
    author_id=data["added_by"]
    added_by=f"<@{author_id}>"
    about=data["about"]
    description=data["description"]
    type=data["type_tags"][0]
    topics=data["topic_tags"]
    role_mention=ROLES[type]["role_id"]
    print(role_mention)
    message=f'''
    `New opportunity in `{role_mention}:
    Added by {added_by}
    TOPICS: `{topics}`
    ```
    {about.strip()}
    ```
    ```
    {description.strip()}
    ```
    '''
    a= await channel.send(message)
    thread=await a.create_thread(name=about)
    await thread.send(added_by)


class AddJob(Modal):
  def __init__(self, title, bot: discord.Bot, ctx: discord.ApplicationContext):
    super().__init__(title=title)
    self.ctx=ctx
    self.bot=bot
    self.add_item(
      InputText(
        label='Job title and short intro*',
        placeholder="Frontend engineer at Sphinx.co",
        required=True,
        max_length=80,
        custom_id='about',
        style=discord.InputTextStyle.short,
      ))
    self.add_item(
      InputText(
        label='Description about the job*',
        placeholder='About...',
        required=True,
        max_length=1000,
        custom_id='description',
        style=discord.InputTextStyle.long,
      ))

  async def callback(self, interaction: discord.Interaction):
    v = DropdownViewPostJob(self.bot)
    await interaction.response.send_message(view=v)
    edit_datajson("job_data","about",self.children[0].value)
    edit_datajson("job_dat","description",self.children[1].value)

class JobTypeDropdown(Select):
  def __init__(self, bot: discord.Bot):
    self.bot = bot
    roles = ROLES.keys()
    options = []
    for role in roles:
      options.append(discord.SelectOption(label=role))

    super().__init__(
      placeholder="Choose type of job",
      min_values=1,
      max_values=1,
      options=options,
    )

  async def callback(self, interaction: discord.Interaction):
    await interaction.response.send_message(f'{self.values}\n')
    edit_datajson("job_data","type_tags",
                  tuple(self.values))  #tuple because python can't hash list


class TopicsDropdown(Select):
  def __init__(self, bot_: discord.Bot):
    self.bot = bot_

    options = [discord.SelectOption(label=l) for l in TOPICS]

    super().__init__(
      placeholder="Choose some topics",
      min_values=1,
      max_values=4,
      options=options,
    )

  async def callback(self, interaction: discord.Interaction):
    await interaction.response.send_message(f'{self.values}\n')
    edit_datajson("job_data","topic_tags",
                  tuple(self.values))  #tuple because python can't hash list
    m=MakeJobMessage(self.bot)
    await m.make_message()

class DropdownViewPostJob(discord.ui.View):
  def __init__(self, bot_: discord.Bot):
    self.bot = bot_
    super().__init__()

    # Adds the dropdown to our View object
    self.add_item(JobTypeDropdown(self.bot))
    self.add_item(TopicsDropdown(self.bot))






class MakeOpportunityMessage():
  def __init__(self,bot: discord.Bot):
    self.bot=bot
    
  async def make_message(self):
    channel=self.bot.get_channel(1079525055844864183) #opportunity channel id
    data=get_datajson("opportunity_data")
    author_id=data["added_by"]
    added_by_mention=f"<@{author_id}>"
    added_by_info=await self.bot.fetch_user(author_id)
    about=data["about"]
    description=data["description"]
    types=data["type_tags"]
    lookingfor= data["looking_for"]
    
    embed = discord.Embed(
            title = about,
            description = description,
            color = discord.Colour.green(),
          )
    embed.set_author(name=added_by_info)
    embed.set_footer(text="by sphinx bot")
    embed.set_thumbnail(url=added_by_info.avatar)
    
    typ=" "
    for type  in types:
      typ+="`{}` ".format(type)  
    embed.add_field(name="Type : ",value=typ)
    embed.add_field(name="Looking for : ",value=lookingfor)
    
    a= await channel.send(embed=embed)
    await a.add_reaction(emoji="✨")
    thread= await a.create_thread(name=about)
    await thread.send(added_by_mention)
    
class AskOpportunity(Modal):
  def __init__(self, title, bot: discord.Bot, ctx: discord.ApplicationContext):
    super().__init__(title=title)
    self.ctx=ctx
    self.bot=bot
    
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
    v = DropdownAskOpportunity(self.bot)
    await interaction.response.send_message(view=v)
    edit_datajson("opportunity_data","about",self.children[0].value)
    edit_datajson("opportunity_data","looking_for",self.children[1].value)
    edit_datajson("opportunity_data","description",self.children[2].value)

class OpportunityTypeDropdown(Select):
  def __init__(self, bot: discord.Bot):
    self.bot = bot
    topics = TOPICS #name should be changed to type and type to role
    options = []
    for topic in topics:
      options.append(discord.SelectOption(label=topic))

    super().__init__(
      placeholder="Choose type of opportunity",
      min_values=1,
      max_values=1,
      options=options,
    )

  async def callback(self, interaction: discord.Interaction):
    await interaction.response.send_message(f'{self.values}\n')
    edit_datajson("opportunity_data","type_tags",
                  tuple(self.values))  #tuple because python can't hash list
    m=MakeOpportunityMessage(self.bot)
    await m.make_message()


class DropdownAskOpportunity(discord.ui.View):
  def __init__(self, bot_: discord.Bot):
    self.bot = bot_
    super().__init__()

    # Adds the dropdown to our View object
    self.add_item(OpportunityTypeDropdown(self.bot))





class mainbot(commands.Cog):

  def __init__(self, bot):
    super().__init__()
    self.bot = bot

  @commands.slash_command(description='Add a job/opportunity')
  async def add_opportunity(self, ctx: discord.ApplicationContext):
    a = AddJob('Submit job/opprtunity',self.bot,ctx)
    await ctx.send_modal(a)
    edit_datajson("job_data","added_by",ctx.author.id)
    

  @commands.slash_command(description='Ask for opportunities')
  async def ask_opportunity(self, ctx: discord.ApplicationContext):
    a = AskOpportunity('Ask for opprtunity',self.bot,ctx)
    await ctx.send_modal(a)
    edit_datajson("opportunity_data","added_by",ctx.author.id)


