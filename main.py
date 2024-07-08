from bot import *
from menus import *
from game import *
from config import TOKEN, GUILD_ID

# Declare intents
intents = discord.Intents.all()

# Instance of your Discord bot in your server
bot = BuckshotBot("!", intents, GUILD_ID)


@bot.tree.command()
async def challenge(interaction: discord.Interaction, player: discord.Member):
    """
    Challenge another user in a gun fight with you

    Parameters
    -----------
    player: discord.Member
        The user that you want to challenge
    """
    author = interaction.user  # The user who used the command

    # You cannot challenge yourself or a bot
    if player.bot:
        await interaction.response.send_message("You cannot challenge a bot!")
    elif player.id == author.id:
        await interaction.response.send_message(
            "Do you really want to kys? :face_with_raised_eyebrow: I don't think so")
    else:  # Valid opponent
        view = YesNoMenu(player)  # Buttons

        # Initialize the players and the game
        p1 = Player(3, author)
        p2 = Player(3, player)
        game = Game(p1, p2)

        await interaction.response.send_message(embed=game.challenge_display(), view=view)  # The display message

        timed_out = await view.wait()  # Check to see if the user reaches timeout

        # Disable all buttons
        view.disable_buttons()
        await interaction.edit_original_response(view=view)

        if timed_out:  # User ran out of time
            await interaction.followup.send(f"**{player.display_name}** ran out of time to decide. "
                                            f"The challenge is cancelled!")
        else:  # User chose a button
            if view.value:  # User chose Yes
                await game.basic_game(interaction)


@bot.command(name="challenge")
async def prf_challenge(ctx: commands.Context, player: discord.Member):
    """
    Challenge another user in a gun fight with you. This command is similar to /challenge

    Parameters
    -----------
    player: discord.Member
        The user that you want to challenge
    """
    # This function use the exact same logic like the challenge() function
    if player.bot:
        await ctx.channel.send("You cannot challenge a bot!")
    elif player.id == ctx.author.id:
        await ctx.channel.send("Do you really want to kys? :face_with_raised_eyebrow: I don't think so")
    else:  # Valid opponent
        view = YesNoMenu(player)  # Buttons

        # Initialize the players and the game
        p1 = Player(3, ctx.author)
        p2 = Player(3, player)
        game = Game(p1, p2)

        display_msg = await ctx.channel.send(embed=game.challenge_display(), view=view)  # The display message

        timed_out = await view.wait()  # Check to see if the user reaches timeout

        # Disable all buttons
        view.disable_buttons()
        await display_msg.edit(view=view)

        if timed_out:  # User ran out of time
            await ctx.channel.send(f"**{player.display_name}** ran out of time to decide. The challenge is cancelled!")
        else:  # User chose a button
            if view.value:  # User chose Yes
                await game.basic_game(ctx)

# Item information for the 2 functions below
item = {
    "Expired Medicine": "Heal 1 - 2 :heart: **LIFE** or lose 1 :heart: **LIFE** but not more than your "
                        "initial :heart: **LIFE**\n",
    "Inverter": "Switch the color of all bullets\n",
    "Cigarette": "Heal 1 :heart: **LIFE** but not more than your initial :heart: **LIFE**\n",
    "Burner Phone": "Reveal the color of a random bullet\n",
    "Adrenaline": "Steal an item from your opponent\n",
    "Magnifying Glass": "Reveal the color of the current bullet\n",
    "Beer": "Eject the current bullet\n",
    "Hand Saw": "Double the damage of the next shot\n",
    "Handcuffs": "Force your opponent to skip their next turn"
}


@bot.tree.command()
async def item_info(interaction: discord.Interaction):
    """Show information about all items available in the game"""
    description = ""
    for name, usage in item.items():
        description += f"**{name}**: {usage}\n"

    await interaction.response.send_message(embed=discord.Embed(
        colour=discord.Colour.purple(),
        title="Item information",
        description=description
    ))


@bot.command(name="item_info")
async def prf_item_info(ctx: commands.Context):
    """Show information about all items available in the game"""
    description = ""
    for name, usage in item.items():
        description += f"**{name}**: {usage}\n"

    await ctx.channel.send(embed=discord.Embed(
        colour=discord.Colour.purple(),
        title="Item information",
        description=description
    ))


@bot.tree.command()
async def advanced_challenge(interaction: discord.Interaction, player: discord.Member):
    """
    Challenge another user in a gun fight with you but with support items

    Parameters
    -----------
    player: discord.Member
        The user that you want to challenge
    """
    author = interaction.user  # The user who used the command

    # You cannot challenge yourself or a bot
    if player.bot:
        await interaction.response.send_message("You cannot challenge a bot!")
    elif player.id == author.id:
        await interaction.response.send_message(
            "Do you really want to kys? :face_with_raised_eyebrow: I don't think so")
    else:  # Valid opponent
        view = YesNoMenu(player)  # Buttons

        # Initialize the players and the game
        hp = random.randint(3, 6)
        p1 = Player(hp, author)
        p2 = Player(hp, player)
        game = Game(p1, p2)

        await interaction.response.send_message(embed=game.challenge_display(), view=view)  # The display message

        timed_out = await view.wait()  # Check to see if the user reaches timeout

        # Disable all buttons
        view.disable_buttons()
        await interaction.edit_original_response(view=view)

        if timed_out:  # User ran out of time
            await interaction.followup.send(f"**{player.display_name}** ran out of time to decide. "
                                            f"The challenge is cancelled!")
        else:  # User chose a button
            if view.value:  # User chose Yes
                await game.basic_game(interaction, True)


@bot.command(name="advanced_challenge")
async def prf_advanced_challenge(ctx: commands.Context, player: discord.Member):
    """
    Challenge another user in a gun fight with you but with support items. This command is similar to
    /advanced_challenge

    Parameters
    -----------
    player: discord.Member
        The user that you want to challenge
    """
    # This function use the exact same logic like the challenge() function
    if player.bot:
        await ctx.channel.send("You cannot challenge a bot!")
    elif player.id == ctx.author.id:
        await ctx.channel.send("Do you really want to kys? :face_with_raised_eyebrow: I don't think so")
    else:  # Valid opponent
        view = YesNoMenu(player)  # Buttons

        # Initialize the players and the game
        hp = random.randint(3, 6)
        p1 = Player(hp, ctx.author)
        p2 = Player(hp, player)
        game = Game(p1, p2)

        display_msg = await ctx.channel.send(embed=game.challenge_display(), view=view)  # The display message

        timed_out = await view.wait()  # Check to see if the user reaches timeout

        # Disable all buttons
        view.disable_buttons()
        await display_msg.edit(view=view)

        if timed_out:  # User ran out of time
            await ctx.channel.send(f"**{player.display_name}** ran out of time to decide. The challenge is cancelled!")
        else:  # User chose a button
            if view.value:  # User chose Yes
                await game.basic_game(ctx, True)

rule = """
- Two players engage in a gunfight (with support items available in advanced mode).\n
- Details about support items can be found using `/item_info`.\n
- Players take turns using items and shooting bullets.\n
- Each player can use multiple items before shooting a bullet.\n
- There are two types of bullets: :red_square: **RED** and :blue_square: **BLUE**.\n
- Each player can decide to shoot themselves or their opponent.\n
- The first player to reach 0 :heart: **LIFE** loses the duel.\n
- Bullets are displayed at the beginning and randomized right after (and reloaded when needed).\n
- A player shot with a :blue_square: **BLUE** bullet will not lose any :heart: **LIFE**.\n
- A player shot with a :red_square: **RED** bullet will lose 1 :heart: **LIFE**.\n
- If a player shoots themselves with a :blue_square: **BLUE** bullet, their turn will continue.
"""


@bot.tree.command()
async def rules(interaction: discord.Interaction):
    """Rules of the game"""
    await interaction.response.send_message(embed=discord.Embed(
        colour=discord.Colour.purple(),
        title="Rules",
        description=rule
    ))


@bot.command(name="rules")
async def prf_rules(ctx: commands.Context):
    """Rules of the game"""
    await ctx.channel.send(embed=discord.Embed(
        colour=discord.Colour.purple(),
        title="Rules",
        description=rule
    ))

# Run the bot
bot.run(TOKEN)
