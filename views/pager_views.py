import discord


class PagerButtonsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.responders_list = list()
        self.embed = discord.Embed(title=" ", color=0x232323)
        self.embed.set_author(name="Participanți")

    @discord.ui.button(label="Răspunde", style=discord.ButtonStyle.blurple, emoji="🚓")
    async def respond(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id in self.responders_list:
            self.responders_list.remove(interaction.user.id)
        else:
            self.responders_list.append(interaction.user.id)
        self.embed.description = '\n'.join(f'<@{resp}>' for resp in self.responders_list)
        await interaction.message.edit(embed=self.embed)

    @discord.ui.button(label="Concluzionează", style=discord.ButtonStyle.green, emoji="✅")
    async def conclude(self, button: discord.ui.Button, interaction: discord.Interaction):
        msg = interaction.message.content.replace('ACTIV', '__**CONCLUZIONAT**__')
        await interaction.message.edit(content=msg, view=None)
        await interaction.response.send_message(f"**{interaction.user.mention}** a __**CONCLUZIONAT**__ pager-ul.")
        self.stop()

    @discord.ui.button(label="Anulează", style=discord.ButtonStyle.grey, emoji="❌")
    async def cancel(self, button: discord.ui.Button, interaction: discord.Interaction):
        msg = interaction.message.content.replace('ACTIV', '__**ANULAT**__')
        await interaction.message.edit(content=msg, view=None)
        await interaction.response.send_message(f"**{interaction.user.mention}** a __**ANULAT**__ pager-ul.")
        self.stop()
