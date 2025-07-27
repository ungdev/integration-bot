import discord 
from discord.ext import commands

from integration_bot.commands import CommandsCog
from integration_bot.events import EventsCog

class Bot(commands.Bot):
  def __init__(self) -> None:
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    super().__init__(command_prefix=commands.when_mentioned, intents=intents)

  async def setup_hook(self) -> None:
    await self.add_cog(CommandsCog(self))
    await self.add_cog(EventsCog(self))

  async def on_ready(self) -> None:
    print(f'Logged in as {self.user} (ID: {self.user.id})')
    print('------')
