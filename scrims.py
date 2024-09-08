import discord
from discord.ext import commands
from database import scrims_collection


class Scrims(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def team_details(self, ctx, team_name: str):
        # fetch details of a team
        team = scrims_collection.find_one({"team_name": team_name})
        if not team:
            await ctx.send("Team not found.")
            return
        embed = discord.Embed(
            title=team["team_name"],
            description=team["description"],
            color=discord.Color.blue(),
        )
        embed.add_field(name="Members", value="\n".join(team["members"]))
        await ctx.send(embed=embed)
