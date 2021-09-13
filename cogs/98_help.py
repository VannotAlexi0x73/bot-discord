import discord
import datetime
from main import config
from discord.ext import commands

class CustomDefaultHelpCommand(commands.DefaultHelpCommand):
    def __init__(self):
        options = {
            'name': "aide",
            'aliases': ["info", "help", "helps", "h"],
            'help': """ Vous permet d'afficher l'aide sur le bot, une commande ou une catégorie.\n
                        __**Format :**__
                        ``!aide [command]``
                        ``!aide [category]``\n
                        __**Exemple :**__
                        ``!aide sondage``
                        ``!h Appel``\n
                    """,
        }
        super().__init__(command_attrs=options)

   # !help
    async def send_bot_help(self, mapping):
        # Usefull variables
        ctx = self.context
        # Create embed with author, footer, commands informations
        embed = discord.Embed(
            color=0x318ce7,
            timestamp=datetime.datetime.utcnow(),
        )
        embed.set_author(
            name="Commandes Lopako",
            icon_url=ctx.bot.user.avatar_url,
        )
        footer_text = "Demandé par " + ctx.author.display_name + " • <> - requis, [] - optionnel"
        embed.set_footer(
            text=footer_text,
            icon_url=ctx.author.avatar_url,
        )
        for cog, commands in mapping.items():
            # We have to use filter_commands() to check if user can see these commands
            filtered_commands = await self.filter_commands(commands)
            command_signatures = [self.get_command_signature(c) for c in filtered_commands]
            if command_signatures:
                cog_qualified_name = getattr(cog, "qualified_name", "Pas de catégorie")
                cog_description = getattr(cog, "description", "Pas de catégorie")
                cog_name = cog_description + " __**" + cog_qualified_name + "**__"
                embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)
        await self.get_destination().send(embed=embed)
        await ctx.message.delete()

   # !help <command>
    async def send_command_help(self, command):
        # Usefull variables
        ctx = self.context
        # Create embed with author, footer, command information
        embed = discord.Embed(
            color=0x87e990,
            timestamp=datetime.datetime.utcnow(),
        )
        title = " Commande :  " + ctx.bot.command_prefix + command.qualified_name
        embed.set_author(
            name=title,
            icon_url=ctx.bot.user.avatar_url,
        )
        footer_text = "Demandé par " + ctx.author.display_name + " • <> - requis, [] - optionnel"
        embed.set_footer(
            text=footer_text,
            icon_url=ctx.author.avatar_url,
        )
        # We have to use filter_commands() to check if user can see these commands
        filtered_command = await self.filter_commands([command])
        if filtered_command:
            embed.description = command.help
            if alias := command.aliases:
                embed.add_field(name="🔑 __**Aliases**__", value=" | ".join(alias), inline=False)
        else:
            embed.add_field(name="🦄 __**403 Forbidden**__", value="Tu ne peux pas voir l'aide de cette commande car tu ne peux pas l'exécuter !", inline=False)
        await self.get_destination().send(embed=embed)
        await ctx.message.delete()

   # !help <cog>
    async def send_cog_help(self, cog):
        # Usefull variables
        ctx = self.context
        # Create embed with author, footer, command information
        embed = discord.Embed(
            color=0xf0c300,
            timestamp=datetime.datetime.utcnow(),
        )
        title = cog.description + " " + cog.qualified_name
        embed.set_author(
            name=title,
            icon_url=ctx.bot.user.avatar_url,
        )
        footer_text = "Demandé par " + ctx.author.display_name + " • <> - requis, [] - optionnel"
        embed.set_footer(
            text=footer_text,
            icon_url=ctx.author.avatar_url,
        )
        # Retrieving commands cog
        filtered_commands = await self.filter_commands(cog.walk_commands())
        commands = [self.get_command_signature(c) for c in filtered_commands]
        if commands:
            embed.add_field(name="📌 __**Commandes**__", value="\n".join(commands), inline=False)
            embed.add_field(name="📁 __**Autres**__", value="Tu peux également exécuter la commande `!help <command>` pour avoir plus d'informations !", inline=False)
        else:
            embed.add_field(name="🦄 __**403 Forbidden**__", value="Il n'y a aucune commande que tu puisses exécuter dans cette catégorie !", inline=False)
        await self.get_destination().send(embed=embed)
        await ctx.message.delete()

   # Error for !help <command>
    async def send_error_message(self, error):
        raise commands.CommandNotFound()


class CustomHelp(commands.Cog, name="Aide", description="💡"):
    def __init__(self, bot):
        self._default_help_command = bot.help_command
        bot.help_command = CustomDefaultHelpCommand()
        bot.help_command.cog = self
        self.bot = bot

    def cog_unload(self):
        self.bot.help_command = self._original_help_command

def setup(bot):
    bot.add_cog(CustomHelp(bot))
