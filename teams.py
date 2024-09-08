import discord
from discord.ext import commands
from database import teams_collection


class Scrims(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def create_team(self, ctx, team_name, description, members):
        team = {
            "team_name": team_name,
            "description": description,
            "members": members,
        }
        teams_collection.insert_one(team)
        return team

    async def update_team(self, ctx, team_name, description, members):
        team = {
            "team_name": team_name,
            "description": description,
            "members": members,
        }
        return team

    async def delete_team(self, ctx, team_name):
        team = {"team_name": team_name}
        return team
