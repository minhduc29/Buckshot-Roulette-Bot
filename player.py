import random
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

    def item_num(self):
        """Return number of items"""
        return sum(self.items.values())

    def reload_item(self):
        """Randomize items for the player"""
        cur_item = self.item_num()
        if cur_item >= 8:
            return
        elif cur_item > 5:
            num = 8 - cur_item
        else:
            num = 3
        for i in range(num):
            item = random.choice(list(self.items))
            self.items[item] += 1
