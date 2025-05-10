import os
import discord
from discord.ext import commands
from discord.ui import Button, View
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
ROLE_ID = int(os.getenv("ROLE_ID"))

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def authpanel(ctx):
    """Send the verification panel with an attached PNG image"""
    button = Button(label="✅ Verify", style=discord.ButtonStyle.success)

    async def button_callback(interaction: discord.Interaction):
        role = ctx.guild.get_role(ROLE_ID)
        if role in interaction.user.roles:
            await interaction.response.send_message("You are already verified.", ephemeral=True)
        else:
            await interaction.user.add_roles(role)
            await interaction.response.send_message("✅ You have been verified! Welcome!", ephemeral=True)

    button.callback = button_callback
    view = View()
    view.add_item(button)

    embed = discord.Embed(
        title="🔒 Verification Panel",
        description="Click the button below to verify yourself.\nOnce verified, you'll gain access to all channels.",
        color=0x00ff00
    )

    # Attach PNG image (must be in same directory)
    embed.set_image(url="attachment://panel.png")
    file = discord.File("panel.png", filename="panel.png")

    await ctx.send(embed=embed, view=view, file=file)

bot.run(TOKEN)
