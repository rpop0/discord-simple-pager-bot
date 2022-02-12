from datetime import datetime

import discord
from discord.commands import slash_command
from discord.commands import ApplicationContext
from discord.ext import commands
from discord.commands import Option
from discord.commands import permissions

from database_managers.pager_manager import PagerManager
from views.pager_views import PagerButtonsView

guild_id = 941703827931922462


class Pager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="add-role", description="Adds a role to the pager.", guild_ids=[guild_id])
    @permissions.has_role("Admin")
    async def add_role_to_pager(self, ctx: ApplicationContext, role_id: Option(str, "Enter the ID of the role."),
                                leader_role_id: Option(str, "Enter the ID of the leader role")) -> None:
        if role_id is None or leader_role_id is None:
            await ctx.send_response("Invalid IDs.")
            return
        await ctx.defer()
        role_normal = ctx.guild.get_role(int(role_id))
        leader_role = ctx.guild.get_role(int(leader_role_id))

        # Get the channel name, category. Create the channel with the permissions.
        channel_name = f"{role_normal.name.lower()}-queue"
        category = discord.utils.get(ctx.guild.categories, name="role queue")
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            leader_role: discord.PermissionOverwrite(read_messages=True)
        }
        await ctx.guild.create_text_channel(channel_name, category=category, overwrites=overwrites)

        # Adds the role to the database.
        async with PagerManager() as pm:
            await pm.add_roles(ctx, int(role_id), int(leader_role_id), role_normal.name, channel_name)

        # Updates the bot role list and updates the internal list.
        await self.bot.update_role_list()

        msg = f"Role {role_normal.name} has been added, with leader role {leader_role}."
        await ctx.send_followup(msg)

    def role_name_helper(self):
        return self.bot.get_roles_as_name_list()

    @slash_command(name="pager", description="Cere o unitate.", guild_ids=[guild_id])
    async def pager(self, ctx: ApplicationContext, unit: Option(str, "Unitati cerute.", autocomplete=role_name_helper),
                    location: Option(str, "Locatia incidentului."), details: Option(str, "Detalii despre incident.")):
        # Pager message
        role_id = discord.utils.get(ctx.guild.roles, name=unit).id
        msg = f"**—PAGER REQUEST—**\n\n**INFO:** {details}\n**DE LA:** <@{ctx.user.id}>\n**CĂTRE:**" \
              f" <@&{role_id}>\n**LOCAȚIE:** {location}\n**STATUS:** ACTIV\n\n**DATA:**" \
              f" {datetime.now().strftime('%m/%b/%Y, %H:%M:%S')}\n**—PAGER REQUEST—** "
        await ctx.send(msg, view=PagerButtonsView())
        await ctx.delete()


def setup(bot):
    bot.add_cog(Pager(bot))
