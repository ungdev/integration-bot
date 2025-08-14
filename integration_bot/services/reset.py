import logging
import discord


async def reset_discord_structure(guild, teams):

    # 1. Retirer le rôle "Nouveau" et "Chef d'équipe"
    nouveau_role = discord.utils.get(guild.roles, name="Nouveau")
    CE_role = discord.utils.get(guild.roles, name="Chef d'équipe")

    if nouveau_role:
        logging.warning(f"[CLEANUP] Removing 'Nouveau' role from members...")
        for member in guild.members:
            if nouveau_role in member.roles:
                await member.remove_roles(nouveau_role)
                logging.warning(f"[CLEANUP] Removed 'Nouveau' from {member.display_name}")
    else:
        logging.warning("[CLEANUP] Role 'Nouveau' not found.")

    if CE_role:
        logging.warning(f"[CLEANUP] Removing 'CE' role from members...")
        for member in guild.members:
            if CE_role in member.roles:
                await member.remove_roles(CE_role)
                logging.warning(f"[CLEANUP] Removed 'Chef d'équipe' from {member.display_name}")
    else:
        logging.warning("[CLEANUP] Role 'Chef d'équipe' not found.")

    # Supprimer les rôles et salons liés aux équipes/factions
    faction_names = set()
    team_names = []


    for team in teams:
        team_name = team.get("name")
        faction_name = team.get("teamFaction", {}).get("name")

        # Ignorer les équipes sans nom ou sans faction
        if team_name == "No name":
            logging.warning(f"[SKIP] Skipping unnamed team with faction '{faction_name}'.")
            continue
        if faction_name == "No faction":
            logging.warning(f"[SKIP] Skipping team '{team_name}' with no faction.")
            continue

        if team_name and faction_name:
            team_names.append(team_name)
            faction_names.add(faction_name)

            # Ignorer les équipes sans nom ou sans faction


    # Supprimer les rôles d’équipe
    logging.warning("[CLEANUP] Deleting team roles...")
    for role in guild.roles:
        if any(team_name in role.name for team_name in team_names):
            await role.delete()
            print(f"[CLEANUP] Deleted team role: {role.name}")

    #Supprimer les rôles de faction
    logging.warning("[CLEANUP] Deleting faction roles...")
    for role in guild.roles:
        if role.name in faction_names:
            await role.delete()
            print(f"[CLEANUP] Deleted faction role: {role.name}")

    # Supprimer les salons et catégories
    logging.warning("[CLEANUP] Deleting faction categories and team channels...")
    for category in guild.categories:
        if category.name in faction_names:
            print(f"[CLEANUP] Deleting category: {category.name}")
            for channel in category.channels:
                await channel.delete()
                print(f"[CLEANUP] Deleted channel: {channel.name}")
            await category.delete()
