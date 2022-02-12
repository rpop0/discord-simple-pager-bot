from datetime import datetime

import discord


class AddRoleButton(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="➕ Cere un rol", style=discord.ButtonStyle.green)
    async def show_role_selection(self, button: discord.ui.Button, interaction: discord.Interaction):
        role_dropdown_view = await AddRoleDropdownView.create(self.bot)
        await interaction.response.send_message("Cere rol", view=role_dropdown_view, ephemeral=True)

    @discord.ui.button(label="➖ Scoate un rol", style=discord.ButtonStyle.red)
    async def show_role_deletion(self, button: discord.ui.Button, interaction: discord.Interaction):
        pass


class ApproveRoleButton(discord.ui.View):
    def __init__(self, requester_interaction: discord.Interaction, role):
        super().__init__(timeout=None)
        self.requester_interaction = requester_interaction
        self.role = discord.utils.get(requester_interaction.guild.roles, name=role)

    @discord.ui.button(label="Accepta cererea", style=discord.ButtonStyle.green)
    async def approve_role(self, button: discord.ui.Button, interaction: discord.Interaction):
        await self.requester_interaction.user.add_roles(self.role)
        await interaction.response.send_message("Cerere acceptata.")
        await interaction.message.edit(view=None)
        self.stop()

    @discord.ui.button(label="Respinge cererea", style=discord.ButtonStyle.red)
    async def deny_role(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Cerere respinsa.")
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
        msg = f"""**[CERERE ROL]**
        Userul {interaction.user} a cerut rolul {self.values[0]}.
        Data: {datetime.now().strftime("%m/%b/%Y, %H:%M:%S")}
        """
        await channel.send(msg, view=ApproveRoleButton(interaction, self.values[0]))
        await interaction.response.send_message(f"{self.values[0]}", ephemeral=True)


class AddRoleDropdownView(discord.ui.View):
    def __init__(self, dropdown):
        super().__init__()
        self.add_item(dropdown)

    @classmethod
    async def create(cls, bot):
        dropdown = await AddRoleDropdown.create(bot)
        return AddRoleDropdownView(dropdown)
