import os
import discord
from colorama import Fore, Style, init

def load_cogs(bot: discord.Bot, directory_name="cogs"):
    """
        Loads all cogs from the specified directory into the bot.

        Args:
            bot (discord.Bot): The bot instance to load cogs into.
            directory_name (str): The name of the directory where the cogs are located.
    """

    if not os.path.isdir(directory_name):
        print(Fore.RED + "[COG ERROR] " + Fore.WHITE + f"The directory '{directory_name}' does not exist.")
        return

    cogs_loaded = 0
    for filename in os.listdir(directory_name):
        if filename.endswith(".py"):
            try:
                bot.load_extension(f"{directory_name}.{filename[:-3]}")
                cogs_loaded += 1
                print(Fore.PURPLE + "[COGS] " + Fore.WHITE + f"Loaded Cog: {filename}")
            except Exception as e:
                print(Fore.RED + "[COG ERROR] " + Fore.WHITE + f"{filename}:\n\n{e}")

    print(Fore.PURPLE + "[COGS] " + Fore.WHITE + f"Successfully loaded {cogs_loaded} cog(s).")
