from abc import ABC
import os

import discord
from discord.ext import commands

from views.role_views import AddRoleButton
from database_managers.pager_manager import PagerManager
from utils.embeds import INIT_MESSAGE_EMBED

intents = discord.Intents.all()


class Bot(commands.Bot, ABC):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('.'), intents=intents)
        self.role_list = None
        self.cog_list = self.get_cog_list()

    def get_roles_as_name_list(self):
        return [role['role_name'] for role in self.role_list]

    def get_channel_on_guild(self, channel_name):
        channel_guild = discord.utils.get(self.get_all_channels(), name=channel_name).guild
        channel_id = discord.utils.get(self.get_all_channels(), name=channel_name).id
        return channel_guild.get_channel(channel_id)

    @staticmethod
    def get_cog_list():
        """
        This static method loops through all of the files in the cogs directory and appends them to a list without
        their .py extension.
        :return: List containing the names of all the cogs.
        """
        cog_list = list()
        for file in os.listdir('./cogs'):
            if file.endswith('.py'):
                cog_list.append(file[:-3])
        return cog_list

    def load_cogs(self):
        for cog in self.cog_list:
            self.load_extension(f'cogs.{cog}')

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
        self.load_cogs()


def main():
    bot = Bot()
    bot.run(os.getenv('BOT_TOKEN'))


if __name__ == '__main__':
    main()
