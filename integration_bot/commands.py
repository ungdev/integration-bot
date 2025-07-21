from discord import app_commands
from discord.ext import commands
import discord

from integration_bot.utils.login import login

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