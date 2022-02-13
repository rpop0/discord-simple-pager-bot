from abc import ABC
from datetime import datetime
import os

import discord
from discord.commands import ApplicationContext
from discord.commands import Option
from discord.commands import permissions
from discord.ext import commands

from views.pager_views import PagerButtonsView
from database_managers.pager_manager import PagerManager

intents = discord.Intents.all()


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

    async def update_role_list(self):
        async with PagerManager() as pm:
            self.role_list = await pm.get_roles()

    async def on_ready(self):
        print("Bot is up.")
        await self.update_role_list()


def main():
    bot = Bot()
    guild_id = int(os.getenv('GUILD_ID'))

    @bot.slash_command(name="add-role", default_permission=False, description="Adds a role to the pager.",
                       guild_ids=[guild_id])
    @permissions.has_any_role("root", "Command Officers", "Staff Officers")
    async def add_role_to_pager(ctx: ApplicationContext, role_id: Option(str, "Enter the ID of the role.")) -> None:
        await ctx.defer()
        if len(role_id) != 18:
            await ctx.send_followup("ID Invalid.")
            return
        role = ctx.guild.get_role(int(role_id))
        # Adds the role to the database.
        async with PagerManager() as pm:
            await pm.add_roles(role.id, role.name)

        # Updates the bot role list and updates the internal list.
        await bot.update_role_list()

        msg = f"Ai adăugat rolul {role.name} la pager!"
        await ctx.send_followup(msg)

    def role_name_helper(ctx):
        return bot.get_role_name_list()

    @bot.slash_command(name="pager", description="Cere o unitate.", guild_ids=[guild_id])
    async def pager(ctx: ApplicationContext, unit: Option(str, "Unitati cerute.", autocomplete=role_name_helper),
                    location: Option(str, "Locatia incidentului."), details: Option(str, "Detalii despre incident.")):
        if ctx.channel.name != "pager":
            await ctx.send_response("Nu poți trimite un pager în acest canal.")
            return
        role_id = discord.utils.get(ctx.guild.roles, name=unit).id
        # Pager message
        msg = f"**—PAGER REQUEST—**\n\n**DE LA:** <@{ctx.user.id}>\n**CĂTRE:** <@&{role_id}>\n" \
              f"**INFO:** {details}\n**LOCAȚIE:** {location}\n**STATUS:** ACTIV\n\n**DATA:**" \
              f" {datetime.now().strftime('%m/%b/%Y, %H:%M:%S')}\n**—PAGER REQUEST—** "
        await ctx.send(msg, view=PagerButtonsView())
        await ctx.delete()

    @bot.slash_command(name="remove-role", default_permissions=False, description="Sterge un rol din pager.",
                       guild_ids=[guild_id])
    @permissions.has_any_role("root", "Command Officers", "Staff Officers")
    async def remove_role(ctx: ApplicationContext, role: Option(str, "Rolul de sters.", autocomplete=role_name_helper)):
        await ctx.defer()
        async with PagerManager() as pm:
            await pm.remove_role(role)
        msg = f"Ai sters rolul {role}"
        await ctx.send_followup(msg)
        await bot.update_role_list()

    bot.run(os.getenv('BOT_TOKEN'))


if __name__ == '__main__':
    main()
