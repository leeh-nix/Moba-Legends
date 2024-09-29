from typing import Literal
import discord
import discord.context_managers
from discord.ext import commands
from database import scrims_collection, teams_collection, members_collection


class Scrims(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # TODO - add user info command
    # @commands.hybrid_command()
    # async def user_info(self, ctx, user_id: int, user_name: str, kda: int):

    # Leaderboard
    @commands.hybrid_command()
    async def leaderboard(
        self,
        ctx: commands.Context,
        filter: Literal["mvp", "loss_mvp", "matches_played"],
        page: int = 1,
    ):
        data = members_collection.find({}).sort(filter, -1)

        embed = discord.Embed(
            title="Leaderboard",
            description="",
            color=discord.Color.blue(),
        )
        embed.set_thumbnail(
            url="https://i.ibb.co/0mWdQz1/leaderboard.pnghttps://learnpython.com/blog/filter-rows-select-in-pandas/cover_hu0e764dad43a837f304bbd0039efe0828_508276_262x262_fill_box_center_2.png"
        )

        embed.set_footer(text=f"Page {page}")
        # embed.set_image(ctx.author.display_avatar.url)

        for index, member in enumerate(data):
            if index >= 10 * (page - 1) and index < 10 * page:
                user = await self.bot.fetch_user(member["user_id"])
                embed.add_field(
                    name=f"{index + 1}. {user.name} - {member[filter]}",
                    # value=f"Matches played: {member['matches_played']}",
                    value=f" ",
                    inline=False,
                )
        await ctx.send(embed=embed)

    # FIXME - "the bot didnt respond"
    # @commands.hybrid_command()
    # async def leaderboard(
    #     self, ctx, metric: Literal["mvp", "loss_mvp", "matches_played"] = "mvp"
    # ):
    #     """
    #     Display the leaderboard sorted by the selected metric in a table format.
    #     Available metrics: mvp, loss_mvp, matches_played
    #     """
    #     # Fetch members from the database
    #     members = list(members_collection.find())

    #     if not members:
    #         await ctx.send("No members found.")
    #         return

    #     # Sort the members based on the chosen metric
    #     if metric == "mvp":
    #         members.sort(key=lambda x: x.get("mvp", 0), reverse=True)
    #     elif metric == "loss_mvp":
    #         members.sort(key=lambda x: x.get("loss_mvp", 0), reverse=True)
    #     elif metric == "matches_played":
    #         members.sort(key=lambda x: x.get("matches_played", 0), reverse=True)

    #     # Table Header
    #     header = f"{'Rank':<5}{'Username':<25}{metric.title():<10}\n"
    #     separator = "-" * (5 + 25 + 10)  # Adjust lengths to match header

    #     # Table Rows
    #     rows = []
    #     for i, member in enumerate(members[:10], start=1):  # Display top 10
    #         discord_username = member.get("discord_username")
    #         metric_value = member.get(metric, 0)

    #         # Format each row to be nicely aligned
    #         row = f"{i:<5}{discord_username:<25}{metric_value:<10}"
    #         rows.append(row)

    #     # Create the full table display
    #     table = f"```{header}{separator}\n" + "\n".join(rows) + "```"

    #     # Send the table as a message
    #     await ctx.send(table)
