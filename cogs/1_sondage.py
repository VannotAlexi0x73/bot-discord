import random
import discord
from discord.ext import commands
from main import config

COLORS = config['colors_list']


class Sondage(commands.Cog, name="Sondage", description="📊"):

    def __init__(self, bot):
        self.bot = bot
        self.last_sondage = None

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 30)
    async def sondage(self, ctx, roles: commands.Greedy[discord.Role]=None, *args):
        """ Vous permet de faire un sondage.\n
            __**Format :**__
            ``!sondage [roles] <args>``
            Le paramètre args doit être sous la forme :
            > ``Question ?;Réponse 1;Réponse 2;...;Réponse 10;$ 5 jours``
            > Il peut y avoir au maximum 10 réponses. Le dernier élement est quant à lui optionnel mais si présent doit obligatoirement commencer par '$'\n
            __**Exemple :**__
            ``!sondage Voulez-vous manger ?;oui;non``
            ``!sondage @role1@role2 Dit-on chocolatine ou pain au chocolat ?;chocolatine;chocolatine;$ 5 jours``\n
        """
        # Get all command values
        command = " ".join(args)
        command_list = command.split(';')
        # Check if end is present
        end_date = command_list[-1]
        if end_date.startswith('$'):
            end_date = end_date.replace('$', '').strip()
            timer = f"Fin du sondage : {end_date}"
            command_list.pop(-1)
        else:
            timer = "Ce sondage est à duré illimité !"
        # Is a correct command ?
        if len(command_list) < 2 or len(command_list) > 11:
            raise commands.UserInputError()
        else:
            if roles is not None:
                description = ''.join([role.mention for role in roles]) + ' ' + command_list[0]
            else:
                description = command_list[0]
            embed = discord.Embed(
                title="**📊 Sondage**",
                description=description,
                color=random.randint(0, 16777215)
            )
            embed.set_author(
                name=ctx.author.display_name,
                icon_url=ctx.author.avatar_url,
            )
            # Delete question from command
            command_list.pop(0)
            # Prepare msg answers
            answers = ""
            for index, answer in enumerate(command_list):
                answers += COLORS[index] + ' ' + answer + "\n"
            embed.add_field(
                name="Réponses :",
                value=answers,
                inline=False,
            )
            embed.set_footer(text=timer)
            await ctx.message.delete()
            message = await ctx.send(embed=embed)
            self.last_sondage = message
            for index in range(len(command_list)):
                await message.add_reaction(COLORS[index])

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(1, 20)
    async def annulerSondage(self, ctx):
        """ Vous permet de supprimer le dernier sondage.\n
            __**Format :**__
            ``!annulerSondage``
            __**Exemple :**__
            ``!annulerSondage``\n
        """
        await ctx.message.delete()
        if self.last_sondage != None:
            await ctx.send("Le sondage vient d'être supprimé !")
            tmp = self.last_sondage
            self.last_sondage = None
            # Delete in last because delete() could raise an exception if message has already been deleted by other member
            await tmp.delete()
        else:
            await ctx.send("Il n'y a pas de sondage a supprimé.")

def setup(bot):
    bot.add_cog(Sondage(bot))
