import discord


class Player:
    """Class that represents a player"""
    def __init__(self, lives, user: discord.Member):
        """Initialize the player"""
        self.max_lives = lives  # The highest number of lives that a player can have
        self.lives = lives  # Number of lives left
        self.turn = False  # If the current turn is this player's turn
        self.items = {  # Support items
            "Expired Medicine": 0,
            "Inverter": 0,
            "Cigarette": 0,
            "Burner Phone": 0,
            "Adrenaline": 0,
            "Magnifying Glass": 0,
            "Beer": 0,
            "Hand Saw": 0,
            "Handcuffs": 0
        }
        self.profile = user  # User information
