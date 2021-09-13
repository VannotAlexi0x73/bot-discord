import discord
from discord.ext import commands
from main import config

MANAGER_ROLE = config['manager_role']


class Admin(commands.Cog, name="Administration", description="🔒"):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(MANAGER_ROLE)
    async def load(self, ctx, extension):
        """ Vous permet de charger une nouvelle extension.\n
            __**Format :**__
            ``!load <extension>``\n
            __**Exemple :**__
            ``!load 2_sondage``\n
        """
        try:
            self.bot.load_extension(f'cogs.{extension}')
            print(f"Extension {extension} has been loaded.")
        except Exception as e:
            print(e) 
        finally:
            await ctx.message.delete()

    @commands.command()
    @commands.has_role(MANAGER_ROLE)
    async def unload(self, ctx, extension):
        """ Vous permet de décharger une extension.\n
            __**Format :**__
            ``!unload <extension>``\n
            __**Exemple :**__
            ``!unload 2_sondage``\n
        """
        try:
            self.bot.unload_extension(f'cogs.{extension}')
            print(f"Extension {extension} has been unloaded.")
        except Exception as e:
            print(e) 
        finally:
            await ctx.message.delete()

    @commands.command()
    @commands.has_role(MANAGER_ROLE)
    async def reload(self, ctx, extension):
        """ Vous permet de recharger extension.\n
            __**Format :**__
            ``!reload <extension>``\n
            __**Exemple :**__
            ``!reload 2_sondage``\n
        """
        try:
            self.bot.unload_extension(f'cogs.{extension}')
            self.bot.load_extension(f'cogs.{extension}')
            print(f"Extension {extension} has been reloaded.")
        except Exception as e:
            print(e) 
        finally:
            await ctx.message.delete()

def setup(bot):
    bot.add_cog(Admin(bot))
