import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD_NAME = (os.getenv('DISCORD_GUILD'))
GUILD_ID = 0

class PostMoogle(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        GUILD = discord.utils.get(client.guilds, name=GUILD_NAME)
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=GUILD)
        print(f'Copying command tree... Please wait')
        await self.tree.sync(guild=GUILD)
        print(f'Copied command tree')

INTENTS = discord.Intents.default()
client = PostMoogle(intents=INTENTS)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    GUILD = discord.utils.get(client.guilds, name=GUILD_NAME)
    print(f'{GUILD.name}(id: {GUILD.id})')
    global GUILD_ID
    GUILD_ID = GUILD.id
    print("Ready!")


@client.tree.command(name="testcommand", description="A test command", guild=discord.Object(id=GUILD_ID))
async def test(interaction: discord.Interaction):
    await interaction.response.send_message("Hello, kupo!")


@client.tree.context_menu(name='Show Join Date')
async def show_join_date(interaction: discord.Interaction, member: discord.Member):
    # The format_dt function formats the date time into a human readable representation in the official client
    await interaction.response.send_message(f'{member} joined at {discord.utils.format_dt(member.joined_at)}')


client.run(TOKEN)