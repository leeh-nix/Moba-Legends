import discord
from discord.ext import commands
from database import members_collection
from typing import Literal, Optional, List
from random import randint


class Scrims(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def create_member(
        self,
        ctx,
        user_name: str,
        role: Literal["Tank", "Fighter", "Assassin", "Marksman", "Mage", "Support"],
        team_name: Optional[str] = None,
    ):
        entry = {
            "user_id": randint(1, 10000),
            "user_name": user_name,
            "role": role,
            "team_name": team_name,
        }
        members_collection.insert_one(entry)
        return entry

    @commands.hybrid_command()
    async def update_member(
        self,
        ctx,
        user_id: int,
        user_name: str,
        role: Literal["Tank", "Fighter", "Assassin", "Marksman", "Mage", "Support"],
        team_name: Optional[str] = None,
    ):
        entry = {"user_name": user_name, "role": role, "team_name": team_name}
        members_collection.update_one(
            filter={"user_id": user_id}, update={"$set": entry}
        )
        return entry

    @commands.hybrid_command()
    async def delete_member(self, ctx, user_id: int, user_name: str):
        members_collection.delete_one(
            filter={"user_id": user_id, "user_name": user_name}
        )
        return f"Deleted user `{user_name}` with user id: `{user_id}`"
