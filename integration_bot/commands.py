from discord import Embed, app_commands
from discord.ext import commands
import discord

from integration_bot.utils.login import login
from integration_bot.utils.teams import get_teams_with_factions
from integration_bot.utils.users import get_teams_with_users

from services.teams import setup_discord_structure
from services.users import assign_roles_to_member
from services.reset import reset_discord_structure

class CommandsCog(commands.Cog):
  def __init__(self, bot: commands.Bot) -> None:
    self.bot = bot

  @commands.is_owner()
  @commands.command(name='sync')
  async def sync_commands(self, ctx: commands.Context) -> None:
    try: 
      await self.bot.tree.sync()
      for guild in self.bot.guilds:
        await self.bot.tree.sync(guild=guild)
      await ctx.send('Commands synced successfully.')
    except app_commands.CommandSyncFailure as e:
      await ctx.send(f'Failed to sync commands: {e}') 

  @commands.is_owner()
  @app_commands.command(name='login')
  async def login_command(self, interaction: discord.Interaction) -> None:
    try:
      token = login()
      await interaction.response.send_message(f'Login successful! Token: {token}')
    except Exception as e:
      await interaction.response.send_message(f'Login failed: {e}')
 
  @commands.is_owner()
  @app_commands.command(name='test')
  async def test_command(self, interaction: discord.Interaction):
    embed = Embed(title="Test OK", description="La commande slash fonctionne parfaitement connard.", color=0x00ff00)
    await interaction.response.send_message(embed=embed)

  @commands.is_owner()
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

  @commands.is_owner()
  @app_commands.command(name="usersync", description="Synchronise les utilisateurs et leurs rôles")
  async def usersync(self, interaction: discord.Interaction) -> None:
    await interaction.response.defer(thinking=True)
    guild = interaction.guild

    try:
      token = login()
      teams = get_teams_with_users(token)
      for member in guild.members:
        await assign_roles_to_member(member, teams)
      await interaction.followup.send("✅ User sync completed successfully.")
    except Exception as e:
      await interaction.followup.send(f"❌ Error during user sync: {str(e)}")


  @commands.is_owner()
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
