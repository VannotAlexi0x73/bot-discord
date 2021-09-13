import discord
import datetime
from main import config
from discord.ext import commands

DEV_ROLE = config['dev_role']


class Others(commands.Cog, name="Autres", description="ℹ️"):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def biographie(self, ctx):
        """ Affiche l'histoire du bot.\n
            __**Format :**__
            ``!info``
            __**Exemple :**__
            ``!info``\n
        """
        biography = """
                Bonjour, je suis Lopako, le robot sur serveur campus CCI,\n
            J'ai été développé par `A.VANNOT` et `V.DONZE`. Ce bot, réalisé dans le cadre d'un projet de deuxième année a pour but de fluidifier les échanges entre les différentes formations au moyen de plusieurs fonctionnalités.\n
            ```Si vous avez des suggestions d'amélioration, il existe une commande "!suggestion Il serait bien d'ajouter cela ...."```
        """
        embed = discord.Embed(
            description=biography,
            color=0xba1c3e,
            timestamp=datetime.datetime.utcnow(),
        )
        embed.set_author(
            name="Biographie",
            icon_url=ctx.bot.user.avatar_url,
        )
        footer_text = "Demandé par " + ctx.author.display_name
        embed.set_footer(
            text=footer_text,
            icon_url=ctx.author.avatar_url,
        )
        await ctx.send(embed=embed)
        await ctx.message.delete()

    @commands.command()
    async def suggestion(self, ctx, *args):
        """ Vous permet d'envoyer des suggestions aux développeurs du BOT afin que vos fonctionnalités soient ajoutées ... ou pas ... 😈\n
            __**Format :**__
            ``!suggestion <args>``
            __**Exemple :**__
            ``!suggestion Il serait intéressant de rajouter ....``\n
        """
        # Get all command values
        suggestion = " ".join(args)

        embed = discord.Embed(
            title="Suggestion",
            description=suggestion,
            color=0xed97f0,
            timestamp=datetime.datetime.utcnow(),
        )
        embed.set_author(
            name=ctx.author.display_name,
            icon_url=ctx.author.avatar_url,
        )

        role = discord.utils.find(lambda r: r.name == DEV_ROLE, ctx.guild.roles)
        for dev in role.members:
            await dev.send(embed=embed)
        await ctx.message.reply("Ta suggestion a bien été envoyée, merci pour ta proposition d'amélioration 💯 !")

def setup(bot):
    bot.add_cog(Others(bot))
