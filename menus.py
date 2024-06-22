import discord
from discord.ext import commands

class YesNoMenu(discord.ui.View):
    def __init__(self, opponent: discord.Member, timeout=60):
        super().__init__(timeout=timeout)
        self.opponent = opponent

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.opponent.id == interaction.user.id:
            await interaction.response.send_message("M gay")
            self.stop()

    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.opponent.id == interaction.user.id:
            await interaction.response.send_message(f"**{interaction.user.display_name}** declined the challenge")          
            self.stop()
