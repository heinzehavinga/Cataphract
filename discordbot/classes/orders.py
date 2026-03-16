import discord
from discord.ext import tasks
from discord import app_commands
from discord.ext import commands 

class OrderSelect(discord.ui.Select):
    def __init__(self):
        options=[
            #KEEP DESCRIPTION UNDER 100 CHARACTERS!
            discord.SelectOption(label="Move",emoji="➡",description="Moves army towards location"),
            discord.SelectOption(label="Forage",emoji="🥪",description="Gather supplies, takes a day"),
            discord.SelectOption(label="Rest",emoji="💤",description="Rest for the said amount of time."),
            discord.SelectOption(label="Operations",emoji="❕",description="A referee will discuss the operation with you and decide how to proceed.")
            ]
        super().__init__(placeholder="Select an option",max_values=1,min_values=1,options=options)
    
    async def callback(self, interaction: discord.Interaction):
        action = self.values[0]

        # disable the select so it can't be used again
        self.disabled = True
        
        print(action)
        if action == "Move":
            await interaction.response.send_modal(DestinationModal())
        else:
            await interaction.response.edit_message(view=self.view)
        

class DestinationModal(discord.ui.Modal, title=f"Set Destination"):
    amount = discord.ui.TextInput(label="Destination", placeholder="hex location (1,2) or known stronghold (Spencerport)")

    async def on_submit(self_inner, modal_interaction: discord.Interaction):
        destination = self_inner.amount.value.strip()
        # basic validation: numeric
        if destination != "Spencerport":
                await modal_interaction.response.send_message("Command not given: Location unknown.", ephemeral=True)
                return

        # handle deposit/withdraw logic here (placeholder)
        await modal_interaction.response.send_message(
            f"You chose a **Move action** with amount **{destination}**.", ephemeral=True
        )




class OrderView(discord.ui.View):
    def __init__(self, *, timeout: float = 60.0):
        super().__init__(timeout=timeout)
        self.add_item(OrderSelect())

    async def on_timeout(self):
        # disable all items on timeout
        self.disable_all_items()
        if hasattr(self, "message") and self.message:
            try:
                await self.message.edit(view=self)
            except Exception:
                pass
