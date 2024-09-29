import discord
from discord.ext import commands
from database import members_collection, maps_collection
from typing import Literal, Optional, List
from random import randint


class Members(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def create_member(
        self,
        ctx,
        discord_username: discord.Member,
        role: Literal["Tank", "Fighter", "Assassin", "Marksman", "Mage", "Support"],
        matches_played: int = 0,
        mvp: int = 0,
        loss_mvp: int = 0,
        team_name: Optional[str] = None,
    ):
        # TODO - check if the user is already registerd
        try:
            # print(discord_username.id)
            entry = {
                "user_id": discord_username.id,
                "role": role,
                "matches_played": matches_played,
                "mvp": mvp,
                "loss_mvp": loss_mvp,
                "team_name": team_name,
            }

            members_collection.insert_one(entry)

            description = (
                f"**User ID:** {entry['user_id']}\n"
                f"**Discord_username:** {discord_username}"
                f"\n**Role:** {role}"
                f"\n**Team:** {team_name}"
            )
            embed = discord.Embed(
                title=f"{discord_username} - {role}",
                description=description,
                color=discord.Color.blue(),
            )
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)
            await ctx.send(f"Error: {e}")

    @commands.hybrid_command()
    async def update_member(
        self,
        ctx,
        discord_username: discord.Member,
        role: Optional[
            Literal["Tank", "Fighter", "Assassin", "Marksman", "Mage", "Support"]
        ],
        matches_played: int = 0,
        mvp: int = 0,
        loss_mvp: int = 0,
        team_name: Optional[str] = None,
    ):
        if mvp and loss_mvp:
            ctx.send("You can't set mvp and loss_mvp at the same time")
            return
        data = members_collection.find_one({"user_id": discord_username.id})
        if data:
            print("BEFORE", data)
            update_data = {}

            if mvp > 0:
                update_data["mvp"] = data["mvp"] + mvp
            if loss_mvp > 0:
                update_data["loss_mvp"] = data["loss_mvp"] + loss_mvp
            if matches_played > 0:
                update_data["matches_played"] = (
                    data.get("matches_played", 0) + matches_played
                )

            update_data["role"] = role
            if team_name:
                update_data["team_name"] = team_name

            print("AFTER", update_data)
            try:
                # Perform the update in MongoDB
                members_collection.update_one(
                    {"user_id": discord_username.id}, {"$set": update_data}
                )
                # TODO - create an embed and display what was updated in bold and what was not
                await ctx.send(
                    f"Updated user `{discord_username}` with user id: `{discord_username.id}`"
                )
            except Exception as e:
                print(e)
                await ctx.send(f"Error: {e}")
        else:
            await ctx.send("User not found")

    @commands.hybrid_command(name="display_member")
    async def get_member(self, ctx, discord_username: discord.Member):
        data = members_collection.find_one({"user_id": discord_username.id})
        if data:
            description = (
                f"**User ID:** {data['user_id']}\n"
                f"**Discord_username:** {discord_username}"
                f"\n**Role:** {data['role']}"
                f"\n**Team:** {data['team_name']}"
            )
            embed = discord.Embed(
                title=f"{discord_username} - {data['role']}",
                description=description,
                color=discord.Color.blue(),
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("User not found")

    @commands.hybrid_command()
    async def delete_member(self, ctx, discord_username: discord.Member):
        print("Yo")
        data = members_collection.find_one({"user_id": discord_username.id})
        if data:
            members_collection.delete_one(filter={"user_id": discord_username.id})
            print("done")

            description = (
                f"Deleted user successfully:\n"
                f"**Discord_username:** `{discord_username}`\n"
                f"**User ID:** `{data['user_id']}`\n"
                f"**Matches played:** `{data['matches_played']}`\n"
                f"**Mvp/loss_mvp:** `{data['mvp']}/{data['loss_mvp']}`\n"
                f"**Role:** `{data['role']}`\n"
                f"**Team:** `{data['team_name']}`"
            )
            # create an embed
            embed = discord.Embed(
                title=f"Deleted user successfully",
                description=description,
                color=discord.Color.red(),
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send("User not found")
