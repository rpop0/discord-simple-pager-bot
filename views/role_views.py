from datetime import datetime

import discord

from utils.embeds import ROLE_DELETION_EMBED, ROLE_ADDITION_EMBED


class AddRoleButton(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="➕ Cere un rol", style=discord.ButtonStyle.green)
    async def show_role_selection(self, button: discord.ui.Button, interaction: discord.Interaction):
        role_dropdown_view = await AddRoleDropdownView.create(self.bot)
        await interaction.response.send_message(" ", embed=ROLE_ADDITION_EMBED, view=role_dropdown_view, ephemeral=True)

    @discord.ui.button(label="➖ Scoate un rol", style=discord.ButtonStyle.red)
    async def show_role_deletion(self, button: discord.ui.Button, interaction: discord.Interaction):
        remove_role_view = await RemoveRoleDropdownView.create(self.bot)
        await interaction.response.send_message(" ", embed=ROLE_DELETION_EMBED, view=remove_role_view, ephemeral=True)


class ApproveRoleButton(discord.ui.View):
    def __init__(self, requester_interaction: discord.Interaction, role):
        super().__init__(timeout=None)
        self.requester_interaction = requester_interaction
        self.role = discord.utils.get(requester_interaction.guild.roles, name=role)

    @discord.ui.button(label="Accepta cererea", style=discord.ButtonStyle.green)
    async def approve_role(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.requester_interaction.user.add_roles(self.role)
        msg = f"**[CERERE ACCEPTATA]** Cererea a fost aceptata de <@{interaction.user.id}> la" \
              f" {datetime.now().strftime('%m/%b/%Y, %H:%M:%S')}"
        await interaction.response.send_message(msg)
        await interaction.message.edit(view=None)
        self.stop()

    @discord.ui.button(label="Respinge cererea", style=discord.ButtonStyle.red)
    async def deny_role(self, button: discord.ui.Button, interaction: discord.Interaction):
        msg = f"**[CERERE RESPINSA]** Cererea a fost respinsa de <@{interaction.user.id}> la" \
              f" {datetime.now().strftime('%m/%b/%Y, %H:%M:%S')}"
        await interaction.response.send_message(msg)
        await interaction.message.edit(view=None)
        self.stop()


class AddRoleDropdown(discord.ui.Select):
    def __init__(self, options, bot):
        super().__init__(options=options)
        self.bot = bot

    @classmethod
    async def create(cls, bot):
        role_list = bot.role_list
        options = list()
        for role in role_list:
            options.append(discord.SelectOption(label=role['role_name'], emoji=role['role_emoji']))
        return AddRoleDropdown(options, bot)

    async def callback(self, interaction: discord.Interaction):
        role_name = self.values[0]
        if discord.utils.get(interaction.user.roles, name=role_name):
            await interaction.response.send_message(f"Ai deja rolul **{role_name}**. Pentru a scoate acest rol, "
                                                    f"foloseste butonul **Scoate un rol**", ephemeral=True)
            return

        channel = discord.utils.get(interaction.guild.channels, name=f"{role_name.lower()}-queue")
        embed = discord.Embed(title=" ", description="Cerere primita pentru acordarea unui rol asupra unui membru al "
                                                     "facțiunii.", color=0xb8b8b8)
        embed.set_author(name="Cerere Rol", icon_url="https://media.discordapp.net/attachments/941661421744291873"
                                                     "/941665577238421544/DISPATCH_CENTER.png")
        embed.set_footer(text="Pentru a accepta sau respinge o cerere, folosește unul dintre butoanele de mai jos.")

        embed.add_field(name="Nume ", value=f"{interaction.user.name}", inline=False)
        embed.add_field(name="Data", value=f"{datetime.now().strftime('%m/%b/%Y, %H:%M:%S')}", inline=False)
        await channel.send(" ", embed=embed, view=ApproveRoleButton(interaction, self.values[0]))
        await interaction.response.send_message(f"Cererea ta a fost trimisă către {self.values[0]} Command. Așteaptă "
                                                f"un răspuns.", ephemeral=True)


class RemoveRoleDropdown(discord.ui.Select):
    def __init__(self, options, bot):
        super().__init__(options=options)
        self.bot = bot

    @classmethod
    async def create(cls, bot):
        role_list = bot.role_list
        options = list()
        for role in role_list:
            options.append(discord.SelectOption(label=role['role_name'], emoji=role['role_emoji']))
        return RemoveRoleDropdown(options, bot)

    async def callback(self, interaction: discord.Interaction):
        role = discord.utils.get(interaction.guild.roles, name=self.values[0])
        if role not in interaction.user.roles:
            await interaction.response.send_message(f"Nu ai rolul {role.name}. ", ephemeral=True)
            return
        await interaction.user.remove_roles(role)
        await interaction.response.send_message(f"Ti-ai scos rolul {role.name}.", ephemeral=True)


class RemoveRoleDropdownView(discord.ui.View):
    def __init(self, dropdown):
        super().__init__()
        self.add_item(dropdown)

    @classmethod
    async def create(cls, bot):
        dropdown = await RemoveRoleDropdown.create(bot)
        return RemoveRoleDropdownView(dropdown)


class AddRoleDropdownView(discord.ui.View):
    def __init__(self, dropdown):
        super().__init__()
        self.add_item(dropdown)

    @classmethod
    async def create(cls, bot):
        dropdown = await AddRoleDropdown.create(bot)
        return AddRoleDropdownView(dropdown)
