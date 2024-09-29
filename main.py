import discord
from discord.ext import commands
import os
from asyncio import run
import dotenv
import tracemalloc


from cogs.members import Members
from cogs.teams import Teams
from cogs.scrims import Scrims
from cogs.sync import Sync

dotenv.load_dotenv()
tracemalloc.start()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

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


bot = commands.Bot(
    command_prefix="bb!", intents=intents, allowed_mentions=allowed_mentions
)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")  # type: ignore
    print("------")


@commands.command()
async def ping(ctx):
    print("pinging")
    await ctx.send("Pong!")


owners = {
    "kokose": 418364415856082954,
    "Yumena": 614278109427925002,
    "Kurama": 476186518172598283,
    "Sandy": 1202766038488322111,
}


async def is_owner(ctx):
    if ctx.author.id in owners.values():
        return True


# @bot.command()
# @commands.check(is_owner)
# async def addOwner(ctx, member: discord.Member):
#     if is_owner(ctx):
#         owners.append(member.id)
#         await ctx.send(f"Added {member} to the owners list")


@bot.command()
async def dmall(ctx, *, message):
    if ctx.author.id not in owners.values():
        await ctx.send("Schade, du hast keine Rechte!")
    else:
        guild = ctx.guild
        print(message, type(message))
        async for member in guild.fetch_members(limit=None):
            try:
                await member.send(message)
            except discord.Forbidden:
                await ctx.send(f"Couldn't send message to {member}")
            except discord.HTTPException as e:
                print("ERROR OCCURED")
                print(f"Failed to send DM to {member.name}: {e}")
            # finally:
            #     await member.ban(reason="DM")


async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.lower() == "yo":
        await message.channel.send("yo yo yo")
    # await bot.process_commands(message)


COGS = [Members, Teams, Scrims, Sync]


async def add_cogs(bot):
    for cog in COGS:
        await bot.add_cog(cog(bot))


EVENTS = [on_message]


def add_events():
    for event in EVENTS:
        bot.add_listener(event)


async def main():
    async with bot:
        add_events()
        await add_cogs(bot)
        if DISCORD_BOT_TOKEN is not None:
            await bot.start(DISCORD_BOT_TOKEN, reconnect=True)
        else:
            print("Error: DISCORD_BOT_TOKEN is not set")


try:
    run(main())
except discord.HTTPException as e:
    if e.status == 429:
        print("The Discord servers denied the connection for making too many requests")
    else:
        raise e
