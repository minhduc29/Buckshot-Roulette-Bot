import discord


class Player:
    """Class that represents a player"""
    def __init__(self, lives, user: discord.Member):
        """Initialize the player"""
        self.lives = lives  # Number of lives left
        self.turn = False  # If the current turn is this player's turn
        self.items = []  # Support items
        self.profile = user  # User information
