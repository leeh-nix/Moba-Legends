import discord
from discord.ext import commands
from typing import Literal, Optional


class Sync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def sync(
        self,
        ctx: commands.Context,
        guilds: commands.Greedy[discord.Object],
        spec: Optional[Literal["~", "*", "^"]] = None,
    ) -> None:
        """
        Synchronize the command tree with one or more guilds.
        Parameters:
            ctx (commands.Context): The context of the command invocation.
            guilds (commands.Greedy[discord.Object]): The guilds to sync with.
            spec (Optional[Literal["~", "*", "^"]]): The sync specification.
                - "~": Sync the entire command tree of the current guild.
                - "*": Copy the global command tree to the current guild and sync.
                - "^": Clear all commands in the current guild and sync.
                If None, sync the entire command tree globally.
        """
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced: list[str] = await ctx.bot.tree.sync()

            synced_commands = [command.name for command in synced]  # type: ignore
            await ctx.send(
                f"```Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}. Synced commands: {', '.join(synced_commands)}```"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")
