import random
import discord
from discord.ext import commands
from player import Player
from menus import ShootMenu
from asyncio import sleep


class Game:
    """Class that represents the game"""
    def __init__(self, p1: Player, p2: Player):
        """Initialize the game"""
        self.p1 = p1  # Player 1
        self.p2 = p2  # Player 2
        self.bullet_number = random.randint(2, 8)  # Number of bullets
        self.over = False  # State of the game
        self.item = {
            "Expired Medicine": "Heal 2 LIFE or lose 1 LIFE but not more than your initial LIFE",
            "Inverter": "Switch the color of the bullet",
            "Cigarette": "Heal 1 LIFE but not more than your initial LIFE",
            "Burner Phone": "Reveal the color of a random bullet",
            "Adrenaline": "Steal an item from your opponent",
            "Magnifying Glass": "Reveal the color of the current bullet",
            "Beer": "Eject the current bullet",
            "Hand Saw": "Double the damage of the next shot",
            "Handcuffs": "Force your opponent to skip their next turn"
        }

        # Number of red bullets
        if self.bullet_number < 4:
            self.red_bullet = random.randint(1, 2)
        else:
            half = int(self.bullet_number / 2)
            self.red_bullet = random.randint(half - 1, half + 1)

        self.blue_bullet = self.bullet_number - self.red_bullet  # Number of blue bullets

        # Represents the gun with all the bullets loaded
        self.gun = ['r' for _ in range(self.red_bullet)] + ['b' for _ in range(self.blue_bullet)]

    async def basic_game(self, interaction_ctx: discord.Interaction | commands.Context):
        """Simulate the basic game"""
        self.first_mover()  # Decide the first player to move
        bullet_embed = self.bullet_display()  # Representation of the bullets
        # Display the bullets
        if isinstance(interaction_ctx, discord.Interaction):  # If it's interaction
            display_msg = await interaction_ctx.followup.send(embed=bullet_embed)
        else:  # If it's context
            display_msg = await interaction_ctx.channel.send(embed=bullet_embed)
        await sleep(5)
        random.shuffle(self.gun)  # Shuffle all the bullets

        while not self.over:  # If the game is not over
            current_player = self.p1 if self.p1.turn else self.p2  # Player to move
            opponent = self.p2 if current_player == self.p1 else self.p1  # Player not to move

            # Main representation of the game
            embed = discord.Embed(
                colour=discord.Colour.from_str("#ff2c55") if current_player == self.p1
                else discord.Colour.from_str("#6ac5fe"),
                description=f"**{current_player.profile.display_name}**\n:heart: **LIFE**: {current_player.lives}"
                            f"\n\n**{opponent.profile.display_name}**\n:heart: **LIFE**: {opponent.lives}"
            )
            embed.set_author(name=f"{current_player.profile.display_name}'s turn",
                             icon_url=current_player.profile.display_avatar.url)

            view = ShootMenu(current_player.profile.id)  # Shoot buttons

            await display_msg.edit(embed=embed, view=view)  # Edit the original embed

            res = await view.wait()  # Check to see if the user reaches timeout

            # Disable all buttons
            view.disable_buttons()
            await display_msg.edit(view=view)
            await sleep(2)

            if res:  # User ran out of time
                if isinstance(interaction_ctx, discord.Interaction):
                    await interaction_ctx.followup.send(
                        f"**{current_player.profile.display_name}** lost due to inactivity!")
                    await interaction_ctx.followup.send(embed=self.winner_display(opponent))
                else:
                    await interaction_ctx.channel.send(
                        f"**{current_player.profile.display_name}** lost due to inactivity!")
                    await interaction_ctx.channel.send(embed=self.winner_display(opponent))
                self.over = True
            else:  # User chose a button
                bullet = self.gun.pop(0)
                self.bullet_number -= 1

                await display_msg.edit(embed=self.round_display(bullet, view.shot_yourself, current_player, opponent),
                                       view=None)  # Display the result of the round
                await sleep(5)

                if view.shot_yourself:  # User chose to shoot himself
                    if bullet == 'r':  # If the bullet is red
                        current_player.lives -= 1  # User lost 1 life
                        if current_player.lives == 0:  # If user dies
                            if isinstance(interaction_ctx, discord.Interaction):
                                await interaction_ctx.followup.send(embed=self.winner_display(opponent))
                            else:
                                await interaction_ctx.channel.send(embed=self.winner_display(opponent))
                            self.over = True  # Game over
                        self.change_turn()
                else:  # User chose to shoot their opponent
                    if bullet == 'r':
                        opponent.lives -= 1
                        if opponent.lives == 0:
                            if isinstance(interaction_ctx, discord.Interaction):
                                await interaction_ctx.followup.send(embed=self.winner_display(current_player))
                            else:
                                await interaction_ctx.channel.send(embed=self.winner_display(current_player))
                            self.over = True
                    self.change_turn()

                # Reload the gun if it runs out of bullets and the game is not over
                if self.bullet_number == 0 and not self.over:
                    self.reload()
                    bullet_embed = self.bullet_display()
                    await display_msg.edit(embed=bullet_embed)
                    await sleep(5)
                    random.shuffle(self.gun)

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

    def first_mover(self):
        """Choose the first player to move randomly"""
        if random.randint(0, 1):
            self.p1.turn = True
        else:
            self.p2.turn = True

    def change_turn(self):
        """Change turn between 2 players"""
        self.p1.turn, self.p2.turn = self.p2.turn, self.p1.turn

    def bullet_display(self):
        """Representation of bullets in the gun"""
        blue = "is" if self.blue_bullet == 1 else "are"
        red = "is" if self.red_bullet == 1 else "are"
        bullet_str = f"There are **{self.bullet_number}** bullets in the gun.\n\n**{self.red_bullet}** of them {red}" \
                     f" **RED**.\n**{self.blue_bullet}** of them {blue} **BLUE**.\n\n"
        for bullet in self.gun:
            bullet_str += ":red_square: " if bullet == 'r' else ":blue_square: "
        return discord.Embed(
            colour=discord.Colour.gold(),
            title="Bullets in the gun",
            description=bullet_str
        )

    def round_display(self, bullet, shot_yourself, player: Player, opponent: Player):
        """Create an embed to display the result of the round"""
        tobe = "is" if self.bullet_number == 1 else "are"  # Grammar
        if bullet == "r":  # If the bullet is red
            if shot_yourself:  # If the player chose to shoot himself
                title = "You shot yourself with a :red_square: RED bullet"
                description = f"**{player.profile.display_name} lost 1 :heart: LIFE.**\n\n"
            else:
                title = "You shot your opponent with a :red_square: RED bullet"
                description = f"**{opponent.profile.display_name} lost 1 :heart: LIFE.**\n\n"
        else:
            if shot_yourself:
                title = "You shot yourself with a :blue_square: BLUE bullet"
                description = "**Next turn is still yours!**\n\n"
            else:
                title = "You shot your opponent with a :blue_square: BLUE bullet"
                description = "**You missed!**\n\n"
        return discord.Embed(
            colour=discord.Colour.brand_red() if bullet == "r" else discord.Colour.blue(),
            title=title,
            description=description + f"There {tobe} **{self.bullet_number}** bullet(s) left.\n"
        )

    def winner_display(self, winner: Player):
        """Create an embed to display the winner"""
        embed = discord.Embed(
            colour=discord.Colour.from_str("#fff46b"),
            description=f"\nChallenge is over!\n\nThe winner is **{winner.profile.display_name}**"
        )
        embed.set_thumbnail(url=winner.profile.display_avatar.url)
        return embed

    def challenge_display(self):
        """Create an embed to display the challenge message"""
        embed = discord.Embed(
            colour=discord.Colour.purple(),
            title="Duckshot Challenge",
            description=f"**{self.p1.profile.display_name}** challenged **{self.p2.profile.display_name}** "
                        f"in a gun fight!\n\nDo you accept this challenge?")
        embed.set_author(name=self.p1.profile.display_name, icon_url=self.p1.profile.display_avatar.url)
        return embed
