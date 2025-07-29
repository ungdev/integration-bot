from discord import Embed, app_commands
from discord.ext import commands
import discord

from integration_bot.utils.login import login
from integration_bot.utils.teams import get_teams_with_factions
from integration_bot.utils.users import get_teams_with_users

from integration_bot.services.teams import setup_discord_structure
from integration_bot.services.users import assign_roles_to_member
from integration_bot.services.reset import reset_discord_structure

class CommandsCog(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot

  @commands.command(name='commandsync')
  async def sync_commands(self, ctx: commands.Context) -> None:
    try: 
      await self.bot.tree.sync()
      for guild in self.bot.guilds:
        await self.bot.tree.sync(guild=guild)
      await ctx.send('Commands synced successfully.')
    except app_commands.CommandSyncFailure as e:
      await ctx.send(f'Failed to sync commands: {e}') 

  @app_commands.command(name='teamsync', description="Synchronise les équipes et factions depuis l'API")
  async def teamsync(self, interaction: discord.Interaction) -> None:
    await interaction.response.defer(thinking=True)
    try:
        token = login()
        teams = get_teams_with_factions(token)
        guild = interaction.guild
        await setup_discord_structure(guild, teams)
        await interaction.followup.send(f"✅ Teams sync successful! {len(teams)} teams processed.")
    except Exception as e:
        await interaction.followup.send(f"❌ Error during sync: {str(e)}")

  @app_commands.command(name="usersync", description="Synchronise les utilisateurs et leurs rôles")
  async def usersync(self, interaction: discord.Interaction) -> None:
    await interaction.response.defer(thinking=True)
    guild = interaction.guild

    try:
      token = login()
      teams = get_teams_with_users(token)
      for member in guild.members:
        await assign_roles_to_member(member, teams, False)
      await interaction.followup.send("✅ User sync completed successfully.")
    except Exception as e:
      await interaction.followup.send(f"❌ Error during user sync: {str(e)}")

  @app_commands.command(name='selfsync', description="Synchronise l'utilisateur qui a exécuté la commande")
  async def usersync_self(self, interaction: discord.Interaction) -> None:
    await interaction.response.defer(thinking=True)

    try:
      token = login()
      teams = get_teams_with_users(token)
      await assign_roles_to_member(interaction.user, teams, True)
      await interaction.followup.send("✅ User sync for yourself completed successfully.")
    except Exception as e:
      await interaction.followup.send(f"❌ Error during user sync for yourself: {str(e)}")

  @app_commands.command(name='cleanupteams', description="Nettoie les rôles, salons et retire le rôle 'Nouveau'")
  async def cleanupteams(self, interaction: discord.Interaction) -> None:
    await interaction.response.defer(thinking=True)
    guild = interaction.guild

    try:
      token = login()
      teams = get_teams_with_factions(token)
      await reset_discord_structure(guild, teams)
      await interaction.followup.send("✅ Cleanup completed successfully.")
    except Exception as e:
      await interaction.followup.send(f"❌ Error during cleanup: {str(e)}")
