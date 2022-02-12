import discord

# Initial message sent in role requests
INIT_MESSAGE_EMBED = discord.Embed(title="Role Request", description="A se folosi doar pentru obținerea rolului "
                                                                     "facțiunii din care faci parte. ", color=0xb8b8b8)
INIT_MESSAGE_EMBED.set_author(name="Dispatch Center", icon_url="https://media.discordapp.net/attachments"
                                                               "/941661421744291873/941665577238421544"
                                                               "/DISPATCH_CENTER.png")
INIT_MESSAGE_EMBED.add_field(name="Pentru ca acest Dispatch să funcționeze corect, fiecare membru al unei facțiuni "
                                  "legale (LSPD; LSFD; JSA; CITY) va trebui să primească rolul aferent facțiunii din "
                                  "care face parte.", value="-----------------", inline=True)
INIT_MESSAGE_EMBED.set_footer(text="Pentru a cere un rol, folosește butonul verde afișat mai jos.")


# Embed that pops up when the deletion is clicked.
ROLE_DELETION_EMBED = discord.Embed(title=" ", description="Pentru a șterge un rol pe care îl aveți, vă puteți folosi "
                                                           "de meniul de mai jos. Va trebui să-l deschideți și să "
                                                           "selectați rolul pe care nu doriți să-l mai aveți.",
                                    color=0xb8b8b8)
ROLE_DELETION_EMBED.set_author(name="Cerere Eliminare Rol", icon_url="https://media.discordapp.net/attachments"
                                                                     "/941661421744291873/941665577238421544"
                                                                     "/DISPATCH_CENTER.png")
ROLE_DELETION_EMBED.set_footer(text="Pentru a anula cererea, folosiți butonul Dismiss Message.")

# Embed that pops up when you request a role.
ROLE_ADDITION_EMBED = discord.Embed(title=" ", description="Deschide meniul afișat mai jos și selectează rolul "
                                                           "facțiunii din care faci parte.", color=0xb8b8b8)
ROLE_ADDITION_EMBED.set_author(name="Selectare rol", icon_url="https://media.discordapp.net/attachments"
                                                              "/941661421744291873/941665577238421544/DISPATCH_CENTER"
                                                              ".png?width=676&height=676")
ROLE_ADDITION_EMBED.set_footer(text="Pentru a anula cererea, folosiți butonul Dismiss Message.")
