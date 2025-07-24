import discord
from discord.ext import commands
from integration_bot.utils.login import login
from integration_bot.utils.users import get_teams_with_users
from integration_bot.services.users import assign_roles_to_member

class EventsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        print(f"[EVENT] Nouveau membre : {member.display_name}")
        try:
            token = login()
            teams = get_teams_with_users(token)
            await assign_roles_to_member(member, teams)
        except Exception as e:
            print(f"[EVENT] Erreur lors de l'attribution des rôles : {e}")