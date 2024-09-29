import os
import discord
from discord.ext import commands

class Cog(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

def setup(bot: discord.Bot):
    bot.add_cog(Cog(bot))
