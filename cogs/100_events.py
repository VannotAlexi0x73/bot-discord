import discord
import datetime
from main import config
from dateutil import tz
from discord.ext import commands
from dateutil.relativedelta import relativedelta


class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Just to warn when bot is online.
    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Game(name="www.aveyron.cci.fr"))
        print('Bot ready.')

    # Arrival of a member.
    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Get channel 'log-arrivants'
        channel = discord.utils.get(self.bot.get_all_channels(), name="log-arrivants")
        if channel:
            # Usefull variables
            created_at = ""
            if member.created_at:
                created_at = self.get_local_datetime_from_utc(member.created_at)
            # Create embed for arrival informations
            description = f"""
            • **Membre :** {member.mention}
            • **Compte crée :** {created_at and created_at.strftime("%d/%m/%Y  à  %H:%M")}
            """
            embed = discord.Embed(
                title="**Arrivée d'un membre**",
                description=description,
                color=0x00ff00,
                timestamp=datetime.datetime.utcnow(),
            )
            embed.set_author(
                name=member.name,
                icon_url=member.avatar_url,
            )
            member_count = self.get_all_members()
            embed.set_footer(text=member_count)
            await channel.send(embed=embed)

    # Leaving of a member.
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # Get channel 'log-arrivants'
        channel = discord.utils.get(self.bot.get_all_channels(), name="log-arrivants")
        if channel:
            # Usefull variables
            joined_at = ""
            if member.joined_at:
                joined_at = self.get_local_datetime_from_utc(member.joined_at)

            utcnow = self.get_local_datetime_from_utc(datetime.datetime.utcnow())

            str_delta = ""
            if joined_at and utcnow:
                delta = relativedelta(utcnow, joined_at)
                # Get the highest value
                if delta.seconds:
                    str_delta = str(delta.seconds) + " seconde(s)"
                if delta.minutes:
                    str_delta = str(delta.minutes) + " minute(s)"
                if delta.hours:
                    str_delta = str(delta.hours) + " heure(s)"
                if delta.days:
                    str_delta = str(delta.days) + " jour(s)"
                if delta.months:
                    str_delta = str(delta.months) + " mois"
                if delta.years:
                    str_delta = str(delta.years) + "an(s)"

            # Create embed for departure informations
            description = f"""
            • **Membre :** {member.mention}
            • **Serveur rejoint le :** {joined_at and joined_at.strftime("%d/%m/%Y  à  %H:%M")}
            • **Serveur quitté le :** {utcnow.strftime("%d/%m/%Y  à  %H:%M")}
            • **Présent depuis :** {str_delta}
            """
            embed = discord.Embed(
                title="**Départ d'un membre**",
                description=description,
                color=0xff0000,
                timestamp=datetime.datetime.utcnow(),
            )
            embed.set_author(
                name=member.name,
                icon_url=member.avatar_url,
            )
            member_count = self.get_all_members()
            embed.set_footer(text=member_count)
            await channel.send(embed=embed)

    def get_all_members(self):
        # Get and return the number of members
        member_count = 0
        for guild in self.bot.guilds:
            member_count += guild.member_count
        member_count = str(member_count) + " Membres"
        return member_count

    def get_local_datetime_from_utc(self, utc):
        # Get zones
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('Europe/Paris')
        # Convert UTC to local
        utc = utc.replace(tzinfo=from_zone)
        return utc.astimezone(to_zone)

def setup(bot):
    bot.add_cog(Events(bot))
