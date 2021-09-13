import os
import sys
import yaml
import discord
from discord.ext import commands
from pprint import pprint


# --------------- Load variables from config.yml ---------------
config = {}
with open("config.yml", 'r') as stream:
    try:
        config.update(yaml.safe_load(stream))
    except:
        print("Unrecoverable error.", file=sys.stderr)
        sys.exit(1)
# --------------------------------------------------------------


def main():
    intent = discord.Intents(messages=True, members=True, guilds=True, reactions=True)
    bot = commands.Bot(command_prefix="!", intents=intent)
    # Load cogs from /cogs
    print("----------------------------")
    filenames = os.listdir('./cogs')
    for filename in filenames:
        if filename.endswith(".py"):
            bot.load_extension(f'cogs.{filename[:-3]}')
            print(f"> Le cog {filename} est chargé !")
    print("----------------------------")
    # pprint all config settings
    pprint(config)
    print("----------------------------")
    bot.run(config['token'])


if __name__ == '__main__':
    main()
