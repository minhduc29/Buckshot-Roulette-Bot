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
    def __init__(self, player_id, item_info=None, player_item=None):
        super().__init__()
        self.player_id = player_id
        self.shot_yourself = None
        self.selected = None
        if item_info and player_item:
            item_menu = ItemMenu(item_info, player_item, player_id, self, False)
            if item_menu.options:  # Add select menu if player has items to use
                self.add_item(item_menu)

    @discord.ui.button(label="Shoot yourself", style=discord.ButtonStyle.primary)
    async def shoot_yourself(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Handle shoot yourself action"""
        if interaction.user.id == self.player_id:
            await interaction.response.defer()
            self.shot_yourself = True
            self.stop()

    @discord.ui.button(label="Shoot opponent", style=discord.ButtonStyle.red)
    async def shoot_opponent(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Handle shoot your opponent action"""
        if interaction.user.id == self.player_id:
            await interaction.response.defer()
            self.shot_yourself = False
            self.stop()

    def disable_buttons(self):
        """Disable all buttons"""
        for button in self.children:
            button.disabled = True


class StealMenu(discord.ui.View):
    def __init__(self, player_id, item_info, opponent_item):
        super().__init__()
        self.player_id = player_id
        self.selected = None
        item_menu = ItemMenu(item_info, opponent_item, player_id, self, True)
        if item_menu.options:  # Add select menu if player has items to use
            self.add_item(item_menu)


class ItemMenu(discord.ui.Select):
    def __init__(self, item_info, player_item, player_id, view: discord.ui.View, steal_menu):
        super().__init__(placeholder="Choose an item to use")
        self.item_info = item_info  # Description of items
        self.player_item = player_item  # Items that the player have
        self.player_id = player_id  # The player that can select the item
        self.parent = view  # The parent view component above this select menu
        self.add_items(steal_menu)  # Add all player items as options to this select menu

    def add_items(self, steal_menu):
        """Add player items as options to this select menu"""
        for item in self.item_info:
            if self.player_item[item]:  # If player has this item
                if steal_menu:  # If this menu is to steal an item from the opponent
                    if item != "Adrenaline":
                        self.add_option(label=item, description=self.item_info[item])
                else:
                    self.add_option(label=item, description=self.item_info[item])

    async def callback(self, interaction: discord.Interaction):
        """Event handler when the player selects an item to use"""
        if interaction.user.id == self.player_id:
            await interaction.response.defer()
            self.parent.selected = self.values[0]
            self.parent.stop()
