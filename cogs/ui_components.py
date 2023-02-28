import discord
from discord.ui import Button, InputText, View, Modal, Select


class myForm(Modal):
    def __init__(self, title, lbl1, lbl2, place_holder1, place_holder2):
        super().__init__(title=title)
        self.add_item(InputText(label=lbl1,
                      placeholder=place_holder1,
                      required=True,
                      max_length=20,
                      custom_id='l1',
                      style=discord.InputTextStyle.short,
                                ))
        self.add_item(InputText(label=lbl2,
                      placeholder=place_holder2,
                      required=True,
                      max_length=200,
                      custom_id='l2',
                      style=discord.InputTextStyle.long,
                                ))


class myButton(Button):
    def __init__(self, label: str, color: str, res: str, emoji, link='',):
        super().__init__(label=label)
        if color.lower == 'red':
            self.style = discord.ButtonStyle.danger
        elif color.lower == 'blurple':
            self.style = discord.ButtonStyle.primary
        elif color.lower == 'green':
            self.style = discord.ButtonStyle.success
        elif color.lower == 'grey':
            self.style = discord.ButtonStyle.secondary
        elif color.lower == 'link':
            self.style = discord.ButtonStyle.link
            self.link = link

        if emoji is not None:
            self.emoji = emoji

    """async def callback(self, interaction=Interaction):
        await interaction.response.send_message('hello there')"""


class myMenu(Select):
    def __init__(self, placeholder: str, options: list = [],max_val=1, min_val=1):
        super().__init__(placeholder=placeholder)
        self.options=options
        self.max_values=max_val
        self.min_values=min_val
      
class SelecOption(discord.SelectOption):
  def __init__(self,label,description):
    self.label=label
    self.description=description


