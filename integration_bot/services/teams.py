import logging
import discord
from integration_bot.utils.slugify import slugify

async def setup_discord_structure(guild: discord.Guild, teams: list):
    # 📦 Caches pour éviter les doublons
    faction_roles = {}
    faction_categories = {}

    # 📋 Récupération des éléments existants
    existing_roles = {role.name: role for role in guild.roles}
    existing_categories = {category.name: category for category in guild.categories}
    existing_channels = {channel.name: channel for channel in guild.channels}

    for team in teams:
        team_name = team.get("name")
        faction_name = team.get("teamFaction", {}).get("name")

        if not team_name or not faction_name:
            logging.warning("[DISCORD] Team ou faction manquante, skipping.")
            continue

        # 🎭 Rôle de faction
        faction_role = faction_roles.get(faction_name) or existing_roles.get(faction_name)
        if not faction_role:
            faction_role = await create_role(guild, faction_name)
        faction_roles[faction_name] = faction_role

        # 🎭 Rôle d'équipe
        team_role_name = f"{team_name} - {faction_name}"
        team_role = existing_roles.get(team_role_name)
        if not team_role:
            team_role = await create_role(guild, team_role_name)

        # 🗂️ Catégorie de faction
        category = faction_categories.get(faction_name) or existing_categories.get(faction_name)
        if not category:
            category = await create_category(guild, faction_name, faction_role)
            faction_categories[faction_name] = category

            # 📣 Salon général de faction
            general_channel_name = f"{faction_name}-général"
            if general_channel_name not in existing_channels:
                await create_text_channel(guild, general_channel_name, category, faction_role)

        # 💬 Salon d’équipe
        team_channel_name = slugify(team_name)
        channel = existing_channels.get(team_channel_name)
        if not channel or channel.category != category:
            await create_text_channel(guild, team_channel_name, category, team_role)
        else:
            logging.info(f"[DISCORD] Salon '{team_channel_name}' déjà existant dans la bonne catégorie.")


# 🔧 Fonctions utilitaires

async def create_role(guild: discord.Guild, name: str) -> discord.Role:
    logging.info(f"[DISCORD] Création du rôle : {name}")
    return await guild.create_role(name=name)

async def create_category(guild: discord.Guild, name: str, role: discord.Role) -> discord.CategoryChannel:
    logging.info(f"[DISCORD] Création de la catégorie : {name}")
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        role: discord.PermissionOverwrite(read_messages=True)
    }
    return await guild.create_category(name=name, overwrites=overwrites)

async def create_text_channel(guild: discord.Guild, name: str, category: discord.CategoryChannel, role: discord.Role):
    logging.info(f"[DISCORD] Création du salon : {name} dans la catégorie {category.name}")
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        role: discord.PermissionOverwrite(read_messages=True)
    }
    await guild.create_text_channel(name=name, category=category, overwrites=overwrites)
