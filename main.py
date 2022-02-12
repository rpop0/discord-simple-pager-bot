from abc import ABC
from datetime import datetime
import os

import discord
from discord.commands import ApplicationContext
from discord.commands import Option
from discord.commands import permissions
from discord.ext import commands
from dotenv import load_dotenv

from views.role_views import AddRoleButton
from views.pager_views import PagerButtonsView
from database_managers.pager_manager import PagerManager
from utils.embeds import INIT_MESSAGE_EMBED

load_dotenv('.env')
intents = discord.Intents.all()
guild_id = int(os.getenv('GUILD_ID'))


class Bot(commands.Bot, ABC):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('.'), intents=intents)
        self.role_list = None

    def get_role_name_list(self):
        return [role['role_name'] for role in self.role_list]

    def get_channel_on_guild(self, channel_name):
        channel_guild = discord.utils.get(self.get_all_channels(), name=channel_name).guild
        channel_id = discord.utils.get(self.get_all_channels(), name=channel_name).id
        return channel_guild.get_channel(channel_id)

    async def send_role_message(self):
        ctx = self.get_channel_on_guild("role-request")

        await ctx.purge()
        view = AddRoleButton(self)
        await ctx.send(embed=INIT_MESSAGE_EMBED, view=view)

    async def update_role_list(self):
        async with PagerManager() as pm:
            self.role_list = await pm.get_roles()

    async def on_ready(self):
        print("Bot is up.")
        await self.update_role_list()
        await self.send_role_message()


def main():
    bot = Bot()

    @bot.slash_command(name="add-role", default_permission=False, description="Adds a role to the pager.",
                       guild_ids=[guild_id])
    @permissions.has_any_role("root", "Management", "Faction Management")
    async def add_role_to_pager(ctx: ApplicationContext, role_id: Option(str, "Enter the ID of the role."),
                                leader_role_id: Option(str, "Enter the ID of the leader role")) -> None:
        await ctx.defer()
        if len(role_id) != 18 or len(leader_role_id) != 18:
            await ctx.send_followup("Invalid IDs.")
            return
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
        await bot.update_role_list()

        msg = f"Role {role_normal.name} has been added, with leader role {leader_role}."
        await ctx.send_followup(msg)

    def role_name_helper(ctx):
        return bot.get_role_name_list()

    @bot.slash_command(name="pager", description="Cere o unitate.", guild_ids=[guild_id])
    async def pager(ctx: ApplicationContext, unit: Option(str, "Unitati cerute.", autocomplete=role_name_helper),
                    location: Option(str, "Locatia incidentului."), details: Option(str, "Detalii despre incident.")):
        # Pager message
        role_id = discord.utils.get(ctx.guild.roles, name=unit).id
        msg = f"**—PAGER REQUEST—**\n\n**DE LA:** <@{ctx.user.id}>\n**CĂTRE:** <@&{role_id}>\n" \
              f"**INFO:** {details}\n**LOCAȚIE:** {location}\n**STATUS:** ACTIV\n\n**DATA:**" \
              f" {datetime.now().strftime('%m/%b/%Y, %H:%M:%S')}\n**—PAGER REQUEST—** "
        await ctx.send(msg, view=PagerButtonsView())
        await ctx.delete()

    bot.run(os.getenv('BOT_TOKEN'))


if __name__ == '__main__':
    main()
