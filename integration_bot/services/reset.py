import logging
import discord

async def reset_discord_structure(guild: discord.Guild, teams: list):
    # 🧹 Suppression des rôles génériques
    await remove_role_from_all_members(guild, "Nouveau")
    await remove_role_from_all_members(guild, "Chef d'équipe")

    # 📦 Collecte des noms d’équipes et de factions
    team_names = []
    faction_names = set()

    for team in teams:
        team_name = team.get("name")
        faction_name = team.get("teamFaction", {}).get("name")

        if not team_name or team_name == "No name":
            logging.warning(f"[SKIP] Équipe sans nom ignorée (faction: {faction_name})")
            continue
        if not faction_name or faction_name == "No faction":
            logging.warning(f"[SKIP] Équipe '{team_name}' sans faction ignorée")
            continue

        team_names.append(team_name)
        faction_names.add(faction_name)

    # 🧨 Suppression des rôles d’équipe et de faction
    await delete_roles(guild, team_names, faction_names)

    # 🧱 Suppression des catégories et salons
    await delete_categories_and_channels(guild, faction_names)


# 🔧 Fonctions utilitaires

async def remove_role_from_all_members(guild: discord.Guild, role_name: str):
    role = discord.utils.get(guild.roles, name=role_name)
    if not role:
        logging.warning(f"[CLEANUP] Rôle '{role_name}' introuvable.")
        return

    logging.info(f"[CLEANUP] Suppression du rôle '{role_name}' pour tous les membres...")
    for member in guild.members:
        if role in member.roles:
            try:
                await member.remove_roles(role)
                logging.info(f"[CLEANUP] Rôle '{role_name}' retiré de {member.display_name}")
            except Exception as e:
                logging.error(f"[CLEANUP] Erreur lors du retrait du rôle '{role_name}' de {member.display_name}: {e}")

async def delete_roles(guild: discord.Guild, team_names: list, faction_names: set):
    logging.info("[CLEANUP] Suppression des rôles d'équipe...")
    for role in guild.roles:
        if any(team_name in role.name for team_name in team_names):
            try:
                await role.delete()
                logging.info(f"[CLEANUP] Rôle d'équipe supprimé : {role.name}")
            except Exception as e:
                logging.error(f"[CLEANUP] Erreur suppression rôle '{role.name}': {e}")

    logging.info("[CLEANUP] Suppression des rôles de faction...")
    for role in guild.roles:
        if role.name in faction_names:
            try:
                await role.delete()
                logging.info(f"[CLEANUP] Rôle de faction supprimé : {role.name}")
            except Exception as e:
                logging.error(f"[CLEANUP] Erreur suppression rôle '{role.name}': {e}")

async def delete_categories_and_channels(guild: discord.Guild, faction_names: set):
    logging.info("[CLEANUP] Suppression des catégories et salons de faction...")
    for category in guild.categories:
        if category.name in faction_names:
            logging.info(f"[CLEANUP] Suppression de la catégorie : {category.name}")
            for channel in category.channels:
                try:
                    await channel.delete()
                    logging.info(f"[CLEANUP] Salon supprimé : {channel.name}")
                except Exception as e:
                    logging.error(f"[CLEANUP] Erreur suppression salon '{channel.name}': {e}")
            try:
                await category.delete()
            except Exception as e:
                logging.error(f"[CLEANUP] Erreur suppression catégorie '{category.name}': {e}")
