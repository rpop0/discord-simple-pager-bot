import discord
from discord.commands import slash_command
from discord.commands import ApplicationContext
from discord.ext import commands
from discord.commands import Option
import time

from database_managers.pager_manager import PagerManager

guild_id = 941703827931922462


class Pager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="hi", description="Hi", guild_ids=[guild_id])
    async def hi(self, ctx: ApplicationContext) -> None:
        await ctx.send_response("test")

    @slash_command(name="add-role", description="Adds a role to the pager.", guild_ids=[guild_id])
    async def add_role_to_pager(self, ctx: ApplicationContext, role_id: Option(str, "Enter the ID of the role."),
                                leader_role_id: Option(str, "Enter the ID of the leader role")) -> None:
        if role_id is None or leader_role_id is None:
            await ctx.send_response("Invalid IDs.")
        await ctx.defer()
        print("here")
        time.sleep(5)
        print("here")
        await ctx.send_response("bepis")
        return

        # role_normal = ctx.guild.get_role(int(role_id))
        # leader_role = ctx.guild.get_role(int(leader_role_id))
        #
        # # Get the channel name, category. Create the channel with the permissions.
        # channel_name = f"{role_normal.name.lower()}-queue"
        # category = discord.utils.get(ctx.guild.categories, name="role queue")
        # overwrites = {
        #     ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        #     leader_role: discord.PermissionOverwrite(read_messages=True)
        # }
        # await ctx.guild.create_text_channel(channel_name, category=category, overwrites=overwrites)
        #
        # # Adds the role to the database.
        # async with PagerManager() as pm:
        #     await pm.add_roles(ctx, int(role_id), int(leader_role_id), role_normal.name, channel_name)
        #
        # await self.bot.update_role_list()
        # msg = f"Role {role_normal.name} has been added, with leader role {leader_role}."
        # await ctx.send_response(msg)


def setup(bot):
    bot.add_cog(Pager(bot))
