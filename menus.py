import discord


class YesNoMenu(discord.ui.View):
    def __init__(self, opponent: discord.Member, timeout=60):
        """Initialize the button menu with yes and no buttons"""
        super().__init__(timeout=timeout)
        self.opponent = opponent  # The user that's being challenged
        self.value = None

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Yes button handling"""
        if self.opponent.id == interaction.user.id:  # Only the opponent can decide
            await interaction.response.send_message(f"**{interaction.user.display_name}** accepted the challenge!")
            self.value = True
            self.stop()

    @discord.ui.button(label="No", style=discord.ButtonStyle.red)
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        """No button handling"""
        if self.opponent.id == interaction.user.id:  # Only the opponent can decide
            await interaction.response.send_message(f"**{interaction.user.display_name}** declined the challenge!")
            self.value = False
            self.stop()

    def disable_buttons(self):
        """Disable all buttons"""
        for button in self.children:
            button.disabled = True


class ShootMenu(discord.ui.View):
    def __init__(self, current_player_id):
        super().__init__()
        self.id = current_player_id
        self.shot_yourself = None

    @discord.ui.button(label="Shoot yourself", style=discord.ButtonStyle.primary)
    async def shoot_yourself(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Handle shoot yourself action"""
        if interaction.user.id == self.id:
            await interaction.response.defer()
            self.shot_yourself = True
            self.stop()

    @discord.ui.button(label="Shoot opponent", style=discord.ButtonStyle.red)
    async def shoot_opponent(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Handle shoot your opponent action"""
        if interaction.user.id == self.id:
            await interaction.response.defer()
            self.shot_yourself = False
            self.stop()

    def disable_buttons(self):
        """Disable all buttons"""
        for button in self.children:
            button.disabled = True
