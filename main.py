from bot import *
from config import TOKEN, GUILD_ID
from menus import *

# Declare intents
intents = discord.Intents.all()

# Instance of your Discord bot in your server
bot = DuckshotBot("!", intents, GUILD_ID)


@bot.tree.command()
async def challenge(interaction: discord.Interaction, player: discord.Member):
    """Challenge another user in a gun fight with you"""
    if player.bot:
        await interaction.response.send_message("You cannot challenge a bot!")
    elif player.id == interaction.user.id:
        await interaction.response.send_message("Do you really want to kys? :face_with_raised_eyebrow: I don't think so")
    else:
        view = YesNoMenu(player)
        embed = discord.Embed(
            colour=discord.Colour.dark_purple(),
            title="Duckshot Challenge",
            description=f"**{interaction.user.display_name}** challenged **{player.display_name}** in a gun fight!"
                        f"\n\nDo you accept this challenge?")
        await interaction.response.send_message(embed=embed, view=view)

# Run the bot
bot.run(TOKEN)
