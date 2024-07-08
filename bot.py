import discord
from discord.ext import commands


class BuckshotBot(commands.Bot):
    def __init__(self, prefix, intents, guild_id=None):
        """Initialize the Discord bot"""
        super().__init__(command_prefix=prefix, intents=intents)
        self.guild_id = guild_id

    async def setup_hook(self):
        """Setting up the bot after log in"""
        if self.guild_id:
            guild = discord.Object(id=self.guild_id)
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)

    async def on_command_error(self, ctx, err):
        """If an error occurs within a normal command"""
        if isinstance(err, commands.MissingRequiredArgument):
            await ctx.send(err)
        elif isinstance(err, commands.CommandNotFound):
            await ctx.send(err)
