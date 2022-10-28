import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from typing import Optional

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
print(TOKEN)
GUILD_NAME = (os.getenv('DISCORD_GUILD'))
print(GUILD_NAME)
GUILD_ID = 1030634128925786162


class PostMoogle(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        GUILD = discord.Object(id=GUILD_ID)
        self.tree.copy_global_to(guild=GUILD)
        print('Copying command tree... Please wait')
        await self.tree.sync(guild=GUILD)
        print('Copied command tree')

INTENTS = discord.Intents.default()
client = PostMoogle(intents=INTENTS)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    GUILD = discord.utils.get(client.guilds, name=GUILD_NAME)
    print(f'{GUILD.name}(id: {GUILD.id})')
    print("Ready!")


@client.tree.command(name="testcommand", description="A test command", guild=discord.Object(id=GUILD_ID))
async def test(interaction: discord.Interaction):
    await interaction.response.send_message("Hello, kupo!")


@client.tree.command(name="deliver", description="Send a secret message with the Postmoogle", guild=discord.Object(id=GUILD_ID))
@app_commands.rename(text_to_send='message')
@app_commands.describe(text_to_send='The message you want the Postmoogle to pass on')
async def deliver(interaction: discord.Interaction, text_to_send: str, member: Optional[discord.Member] = None, channel: Optional[discord.TextChannel] = None):
    # If no member is explicitly provided then we use the command user here
    member = member or interaction.user
    channel = channel or interaction.channel
    await channel.send(f'{member.mention}\nYou have a message, kupo!\n\n"{text_to_send}"')
    await interaction.response.send_message("I'll do my best to deliver your message, kupo!", ephemeral=True)


@client.tree.command()
@app_commands.describe(member='The member you want to get the joined date from; defaults to the user who uses the command')
async def joined(interaction: discord.Interaction, member: Optional[discord.Member] = None):
    """Says when a member joined."""
    member = member or interaction.user

    # The format_dt function formats the date time into a human readable representation in the official client
    await interaction.response.send_message(f'{member} joined {discord.utils.format_dt(member.joined_at)}')


client.run(TOKEN)