import discord
from discord.ext import commands
from main import config

DELETE_DELAY = config['time_to_delete_msg']


class Errors(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Error handling
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """ Function that returns embeded error message.
        https://discordpy.readthedocs.io/en/stable/ext/commands/api.html#exception-hierarchy """

        if isinstance(error, commands.CommandNotFound):
            message = "Oh ! Cette commande n'existe pas ☄️ !"
        elif isinstance(error, commands.NoPrivateMessage):
            message = "Hé ! Vous ne pouvez pas utiliser cette commande ici... 🤪 !"
        elif isinstance(error, commands.CommandOnCooldown):
            message = f"Cette commande est en cooldown. Merci d'essayer dans {round(error.retry_after, 1)} secondes ⏳."
        elif isinstance(error, commands.MissingRole):
            message = "Tu n'as pas les droits pour lancer cette commande 👮‍♂️ !"
        elif isinstance(error, commands.UserInputError):
            message = "Ah ! Je t'invite à lire l'aide de la commande en faisant !aide <command> et de réessayer 📋 !"
        elif isinstance(error, commands.DisabledCommand):
            message = "Désolé ! Cette commande est désactivée ❌."
        elif isinstance(error, commands.CommandInvokeError):
            # No message here, tyring to delete private msg
            print("Error (commands.CommandInvokeError) : ", error)
            return
        else:
            message = "Oh non ! Une erreur s'est produite lors de l'exécution de la commande ! Merci de le remonter aux responsables 🛠."

        # Delay in seconds
        embed = discord.Embed(
            title="**⚠️ Erreur**",
            description=message,
            color=0x9e0e40
        )
        await ctx.send(embed=embed, delete_after=DELETE_DELAY)
        await ctx.message.delete(delay=DELETE_DELAY)

def setup(bot):
    bot.add_cog(Errors(bot))
