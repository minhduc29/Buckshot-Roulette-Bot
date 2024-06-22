from bot import *
from menus import *
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
        await interaction.response.send_message("Do you really want to kys? :face_with_raised_eyebrow: I don't think so")
    else:  # Valid opponent
        view = YesNoMenu(player)  # Buttons
        embed = discord.Embed(
            colour=discord.Colour.dark_purple(),
            title="Duckshot Challenge",
            description=f"**{author.display_name}** challenged **{player.display_name}** in a gun fight!"
                        f"\n\nDo you accept this challenge?")
        embed.set_author(name=author.display_name, icon_url=author.display_avatar.url)
        await interaction.response.send_message(embed=embed, view=view)  # The display message

        res = await view.wait()  # Check to see if the user reaches timeout

        # Disable all buttons
        for btn in view.children:
            btn.disabled = True
        await interaction.edit_original_response(view=view)

        if res:  # User ran out of time
            await interaction.followup.send("You ran out of time to decide. The challenge is cancelled!")
        else:  # User accepted the challenge
            pass

# Run the bot
bot.run(TOKEN)
