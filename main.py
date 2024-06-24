from bot import *
from menus import *
from game import *
from config import TOKEN, GUILD_ID

# Declare intents
intents = discord.Intents.all()

# Instance of your Discord bot in your server
bot = DuckshotBot("!", intents, GUILD_ID)


@bot.tree.command()
async def challenge(interaction: discord.Interaction, player: discord.Member):
    """Challenge another user in a gun fight with you"""
    author = interaction.user  # The user who used the command

    # You cannot challenge yourself or a bot
    if player.bot:
        await interaction.response.send_message("You cannot challenge a bot!")
    elif player.id == author.id:
        await interaction.response.send_message(
            "Do you really want to kys? :face_with_raised_eyebrow: I don't think so")
    else:  # Valid opponent
        view = YesNoMenu(player)  # Buttons
        embed = discord.Embed(
            colour=discord.Colour.purple(),
            title="Duckshot Challenge",
            description=f"**{author.display_name}** challenged **{player.display_name}** in a gun fight!"
                        f"\n\nDo you accept this challenge?")
        embed.set_author(name=author.display_name, icon_url=author.display_avatar.url)
        await interaction.response.send_message(embed=embed, view=view)  # The display message

        res = await view.wait()  # Check to see if the user reaches timeout

        # Disable all buttons
        view.disable_buttons()
        await interaction.edit_original_response(view=view)

        if res:  # User ran out of time
            await interaction.followup.send(f"**{player.display_name}** ran out of time to decide. "
                                            f"The challenge is cancelled!")
        else:  # User chose a button
            if view.value:  # User chose Yes
                p1 = Player(3, interaction.user)
                p2 = Player(3, player)
                game = Game(p1, p2)
                await game.basic_game(interaction)


@bot.command(name="challenge")
async def prf_challenge(ctx: commands.Context,
                        player: discord.Member = commands.parameter(description="The user that you want to challenge")):
    """
    Challenge another user in a gun fight with you
    This command is similar to /challenge
    """
    # This function use the exact same logic like the challenge() function
    if player.bot:
        await ctx.channel.send("You cannot challenge a bot!")
    elif player.id == ctx.author.id:
        await ctx.channel.send("Do you really want to kys? :face_with_raised_eyebrow: I don't think so")
    else:  # Valid opponent
        view = YesNoMenu(player)  # Buttons
        embed = discord.Embed(
            colour=discord.Colour.purple(),
            title="Duckshot Challenge",
            description=f"**{ctx.author.display_name}** challenged **{player.display_name}** in a gun fight!"
                        f"\n\nDo you accept this challenge?")
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
        display_msg = await ctx.channel.send(embed=embed, view=view)  # The display message

        res = await view.wait()  # Check to see if the user reaches timeout

        # Disable all buttons
        view.disable_buttons()
        await display_msg.edit(view=view)

        if res:  # User ran out of time
            await ctx.channel.send(f"**{player.display_name}** ran out of time to decide. The challenge is cancelled!")
        else:  # User chose a button
            if view.value:  # User chose Yes
                p1 = Player(3, ctx.author)
                p2 = Player(3, player)
                game = Game(p1, p2)
                await game.basic_game(ctx)

# Run the bot
bot.run(TOKEN)
