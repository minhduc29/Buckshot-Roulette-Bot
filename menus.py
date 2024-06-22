import discord


class YesNoMenu(discord.ui.View):
    def __init__(self, opponent: discord.Member, timeout=60):
        """Initialize the button menu with yes and no buttons"""
        super().__init__(timeout=timeout)
        self.opponent = opponent  # The user that's being challenged

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Yes button handling"""
        if self.opponent.id == interaction.user.id:  # Only the opponent can decide
            await interaction.response.send_message(f"**{interaction.user.display_name}** accepted the challenge!")
            self.stop()

    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        """No button handling"""
        if self.opponent.id == interaction.user.id:  # Only the opponent can decide
            await interaction.response.send_message(f"**{interaction.user.display_name}** declined the challenge!")
            self.stop()
