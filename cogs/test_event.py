import discord
from discord.ui import InputText, View, Modal
from discord.ext import commands
from json_edit import edit_datajson, get_datajson
from vals import EVENTS_NOTIF_CHANNEL
import datetime

EVENT_ROLE_ID = 1079524515995996180
GENERAL_CHANNEL_ID=743164013126615112

class MakeEventMessage():

  def __init__(self, bot: discord.Bot):
    self.bot = bot

  async def make_message(self):
    channel = self.bot.get_channel(
      743164013126615112)
    general_channel=self.bot.get_channel(
      GENERAL_CHANNEL_ID)
    data = get_datajson("event_data")
    author_id = data["added_by"]
    author_mention = f"<@{author_id}>"
    author_info = await self.bot.fetch_user(author_id)
    about = data["about"]
    description = data["event_details"]
    date = data["date"]
    time = data["time"]
    role_mention = "<@&{}>".format(EVENT_ROLE_ID)
    thumbnail_img= data["thumbnail_link"].strip()

    embed = discord.Embed(title=about,
                          description=description,
                          color=discord.Colour.yellow(),
                          timestamp=datetime.datetime.utcnow())
    embed.set_author(name=author_info)
    embed.set_footer(text="via pyramid")
    embed.add_field(name="Created by : ",value= author_mention)
    embed.add_field(name="\nDate: \n", value=date)
    embed.add_field(name="\nTime: \n", value=time, inline=False)
    try:
      embed.set_image(
        url= thumbnail_img)
    except Exception:
      embed.set_image(
        url=
        'https://cdn.discordapp.com/attachments/560753089179680768/594957849797460177/Epic_gif-1.gif'
      )

    
    a = await channel.send(embed=embed)
    await a.add_reaction(emoji="⬆️")
    thread = await a.create_thread(name=about)
    edit_datajson("event_data", "thread_link", thread.jump_url)
    await thread.send(author_mention)
    await thread.send(role_mention)

    general_embed = discord.Embed(title=about,
                          description=description,
                          color=discord.Colour.yellow(),
                          timestamp=datetime.datetime.utcnow())
    general_embed.set_footer(text="via pyramid")
    general_embed.add_field(name="Created by : ",value= author_mention)
    general_embed.add_field(name="\nDate: \n", value=date, inline=False)
    general_embed.add_field(name="\nTime: \n", value=time)
    general_embed.add_field(name=f'[jump to message]({a.jump_url})',value="",inline=False)

    await general_channel.send(embed=general_embed)


class CreateEvent(Modal):

  def __init__(self, title, bot: discord.Bot, ctx: discord.ApplicationContext):
    super().__init__(title=title)
    self.ctx = ctx
    self.bot = bot
    self.add_item(
      InputText(
        label='What is the event about?',
        required=True,
        max_length=100,
        custom_id='about',
        style=discord.InputTextStyle.short,
      ))
    self.add_item(
      InputText(
        label='Tell us more about it',
        required=True,
        max_length=300,
        custom_id='event_details',
        style=discord.InputTextStyle.long,
      ))
    self.add_item(
      InputText(
        label='Date {weekday} {date}',
        placeholder='Sunday 05.03.2023',
        required=True,
        max_length=20,
        custom_id='date',
        style=discord.InputTextStyle.short,
      ))
    self.add_item(
      InputText(
        label='Time? [12 hour format] [in IST]',
        placeholder='3:00 pm',
        required=True,
        max_length=8,
        custom_id='time',
        style=discord.InputTextStyle.short,
      ))
    self.add_item(
      InputText(
        label='Link for event thumbnail image (optional)',
        placeholder='must start with https:// and end in .png or .jpg',
        required=False,
        max_length=200,
        custom_id='link',
        style=discord.InputTextStyle.short,
      )
    )

  async def callback(self, interaction: discord.Interaction):
    await interaction.response.defer()
    edit_datajson("event_data", "about", self.children[0].value)
    edit_datajson("event_data", "event_details", self.children[1].value)
    edit_datajson("event_data", "date", self.children[2].value)
    edit_datajson("event_data", "time", self.children[3].value)
    edit_datajson("event_data", "thumbnail_link", self.children[4].value)
    

    m = MakeEventMessage(self.bot)
    await m.make_message()


class EventCommands(commands.Cog):

  def __init__(self, bot):
    super().__init__()
    self.bot = bot

  @commands.slash_command(description='Create events')
  async def event_create(self, ctx: discord.ApplicationContext):
    a = CreateEvent("Create an event",self.bot,ctx)
    await ctx.send_modal(a)
    edit_datajson("event_data", "added_by", ctx.author.id)


def setup(bot):
  bot.add_cog(EventCommands(bot))
