
import logging
import discord
from integration_bot.utils.slugify import slugify


async def setup_discord_structure(guild, teams):
    faction_roles = {}
    faction_categories = {}

    # Récupérer les rôles, catégories et salons existants
    existing_roles = {role.name: role for role in guild.roles}
    existing_categories = {category.name: category for category in guild.categories}
    existing_channels = {channel.name: channel for channel in guild.channels}

    for team in teams:
        team_name = team.get("name", "No name")
        faction_name = team.get("teamFaction", {}).get("name", "No faction")

        if team_name == "No name" or faction_name == "No faction":
            continue

        # Créer le rôle de faction une seule fois
        faction_role = existing_roles.get(faction_name)
        if not faction_role:
            logging.warning(f"[DISCORD] Creating faction role: {faction_name}")
            faction_role = await guild.create_role(name=faction_name)

        # Créer le rôle d’équipe une seule fois
        role_name = f"{team_name} - {faction_name}"
        team_role = existing_roles.get(role_name)
        if not team_role:
            logging.warning(f"[DISCORD] Creating team role: {role_name}")
            team_role = await guild.create_role(name=role_name)

        # Créer la catégorie si elle n'existe pas
        if faction_name not in faction_categories:
            category = existing_categories.get(faction_name)
            if not category:
                logging.warning(f"[DISCORD] Creating category for faction: {faction_name}")
                category = await guild.create_category(
                    faction_name,
                    overwrites={
                        guild.default_role: discord.PermissionOverwrite(read_messages=False),
                        faction_role: discord.PermissionOverwrite(read_messages=True)
                    }
                )
                # Créer un salon général pour la faction
                general_channel_name = f"{faction_name}-général"
                if general_channel_name not in existing_channels:
                    logging.warning(f"[DISCORD] Creating general channel for faction: {faction_name}")
                    await guild.create_text_channel(
                        name=general_channel_name,
                        category=category,
                        overwrites={
                            guild.default_role: discord.PermissionOverwrite(read_messages=False),
                            faction_role: discord.PermissionOverwrite(read_messages=True)
                        }
                    )
            faction_categories[faction_name] = category
        else:
            category = faction_categories[faction_name]

        # Créer le salon d’équipe
        team_channel_name = slugify(team_name)
        existing_channel = existing_channels.get(team_channel_name)
        if not existing_channel or existing_channel.category != category:
            logging.warning(f"[DISCORD] Creating channel for team: {team_name} in faction: {faction_name}")
            await guild.create_text_channel(
                name=team_channel_name,
                category=category,
                overwrites={
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    team_role: discord.PermissionOverwrite(read_messages=True)
                }
            )
        else:
            logging.warning(f"[DISCORD] Channel '{team_channel_name}' already exists in correct category. Skipping.")

