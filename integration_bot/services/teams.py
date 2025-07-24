import discord

async def setup_discord_structure(guild, teams):
    faction_roles = {}
    faction_categories = {}

    for team in teams:
        team_name = team.get("name", "No name")
        faction_name = team.get("teamFaction", {}).get("name", "No faction")

        if team_name == "No name" or faction_name == "No faction":
            continue

        # Créer le rôle de faction une seule fois
        if faction_name not in faction_roles:
            print(f"[DISCORD] Creating faction role: {faction_name}")
            faction_role = await guild.create_role(name=faction_name)
            faction_roles[faction_name] = faction_role
        else:
            faction_role = faction_roles[faction_name]

        #Créer le rôle d’équipe
        role_name = f"{team_name} - {faction_name}"
        print(f"[DISCORD] Creating team role: {role_name}")
        team_role = await guild.create_role(name=role_name)

        #Créer la catégorie si elle n'existe pas
        if faction_name not in faction_categories:
            print(f"[DISCORD] Creating category for faction: {faction_name}")
            category = await guild.create_category(
                faction_name,
                overwrites={
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    faction_role: discord.PermissionOverwrite(read_messages=True)
                }
            )
            faction_categories[faction_name] = category

            #Créer un salon général pour la faction
            print(f"[DISCORD] Creating general channel for faction: {faction_name}")
            await guild.create_text_channel(
                name=f"{faction_name}-général",
                category=category,
                overwrites={
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    faction_role: discord.PermissionOverwrite(read_messages=True)
                }
            )
        else:
            category = faction_categories[faction_name]

        #Créer le salon d’équipe
        print(f"[DISCORD] Creating channel for team: {team_name} in faction: {faction_name}")
        await guild.create_text_channel(
            name=team_name,
            category=category,
            overwrites={
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                team_role: discord.PermissionOverwrite(read_messages=True)
            }
        )
        
