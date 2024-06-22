import random
from player import Player


class Game:
    """Class that represents the game"""
    def __init__(self, p1: Player, p2: Player):
        """Initialize the game"""
        self.p1 = p1  # Player 1
        self.p2 = p2  # Player 2
        self.bullet_number = random.randint(2, 8)  # Number of bullets
        self.over = False  # State of the game

        # Number of red bullets
        if self.bullet_number < 4:
            self.red_bullet = random.randint(1, 2)
        else:
            half = int(self.bullet_number / 2)
            self.red_bullet = random.randint(half - 1, half + 1)

        self.blue_bullet = self.bullet_number - self.red_bullet  # Number of blue bullets

        # Represents the gun with all the bullets loaded
        self.gun = ['r' for _ in range(self.red_bullet)] + ['b' for _ in range(self.blue_bullet)]

    def reload(self):
        """Reload the gun with a new set of bullets"""
        self.bullet_number = random.randint(2, 8)
        if self.bullet_number < 4:
            self.red_bullet = random.randint(1, 2)
        else:
            half = int(self.bullet_number / 2)
            self.red_bullet = random.randint(half - 1, half + 1)
        self.blue_bullet = self.bullet_number - self.red_bullet
        self.gun = ['r' for _ in range(self.red_bullet)] + ['b' for _ in range(self.blue_bullet)]
