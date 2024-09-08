import discord

import os
import dotenv

dotenv.load_dotenv()

URI = os.getenv("DATABASE_URI")

intents = discord.Intents(
    guilds=True,
    members=True,
    presences=True,
    messages=True,
    reactions=True,
    emojis=True,
    invites=True,
    voice_states=True,
    message_content=True,
)
allowed_mentions = discord.AllowedMentions(everyone=False, roles=True)


# Create a new client and connect to the server
