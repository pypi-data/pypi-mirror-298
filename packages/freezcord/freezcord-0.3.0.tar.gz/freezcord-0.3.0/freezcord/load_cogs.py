import os
import discord
from colorama import Fore, Style, init

def load_cogs(bot: discord.Bot, directory_name="cogs"):
    """
    Loads all cogs from the specified directory into the bot.

    Args:
        bot (discord.Bot): The bot object that should load the cogs.
        directory_name (str): The name of the directory where the cogs are located.
    """

    cogs_loaded = 0
    for filename in os.listdir(directory_name):
        if filename.endswith(".py"):
            try:
                bot.load_extension(f"{directory_name}.{filename[:-3]}")
                cogs_loaded += 1
                print(f"Loaded cog: {filename}")
            except Exception as e:
                print(f"Error loading cog {filename}: {e}")
                return

    print(Fore.PURPLE+"[COGS] "+"Successfully loaded {cogs_loaded} cog(s).")

