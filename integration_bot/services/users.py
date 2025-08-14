import discord
import logging
from integration_bot.utils.slugify import slugify

async def assign_roles_to_member(member: discord.Member, teams: list, mp: bool):
    discord_id = str(member.id)
    guild = member.guild

    # 🔍 Recherche de l'utilisateur et de son équipe
    user_found, team = find_user_and_team(discord_id, teams)

    if not user_found:
        if mp:
            await send_sync_message(member)
        logging.warning(f"[DISCORD] Aucun utilisateur trouvé pour {member.display_name}")
        return

    if not team:
        logging.warning(f"[DISCORD] Aucun équipe associée à l'utilisateur {member.display_name}")
        return

    logging.warning(f"[DISCORD] Utilisateur trouvé : {user_found}")
    logging.warning(f"[DISCORD] Équipe trouvée : {team}")

    # 🎭 Attribution des rôles
    roles_to_assign = get_roles_to_assign(guild, team, user_found)
    await assign_roles(member, roles_to_assign)

    # 🧾 Mise à jour du pseudo
    await update_nickname(member, user_found)


# 🔧 Fonctions utilitaires

def find_user_and_team(discord_id: str, teams: list):
    for team in teams:
        logging.debug(f"[RECHERCHE] Team scannée : {team.get('name')}")
        for user in team.get("users", []):
            if user.get("discordId") == discord_id:
                return user, team
    return None, None

async def send_sync_message(member: discord.Member):
    try:
        await member.send("Bienvenue ! Pour accéder aux rôles, synchronise ton compte ici : https://integration.utt.fr/Profil")
    except Exception as e:
        logging.warning(f"[DISCORD] Erreur d'envoi du message privé : {e}")

def get_roles_to_assign(guild: discord.Guild, team: dict, user: dict):
    roles = []

    team_name = team.get("name", "No name")
    faction_name = team.get("faction", "No faction")

    team_role_name = f"{team_name} - {faction_name}"
    faction_role_name = faction_name

    logging.debug(f"[DISCORD] Rôles recherchés : {team_role_name}, {faction_role_name}")

    team_role = discord.utils.get(guild.roles, name=team_role_name)
    faction_role = discord.utils.get(guild.roles, name=faction_role_name)

    if team_role:
        roles.append(team_role)
    else:
        logging.warning(f"[DISCORD] Rôle d'équipe introuvable : {team_role_name}")

    if faction_role:
        roles.append(faction_role)
    else:
        logging.warning(f"[DISCORD] Rôle de faction introuvable : {faction_role_name}")

    permission = user.get("permission")
    if permission == "Nouveau":
        role = discord.utils.get(guild.roles, name="Nouveau")
    elif permission == "Student":
        role = discord.utils.get(guild.roles, name="Chef d'équipe")
    else:
        role = None

    if role:
        roles.append(role)

    return roles

async def assign_roles(member: discord.Member, roles: list):
    if not roles:
        logging.warning(f"[DISCORD] Aucun rôle à attribuer à {member.display_name}")
        return
    try:
        await member.add_roles(*roles)
        logging.info(f"[DISCORD] Rôles attribués à {member.display_name}: {[r.name for r in roles]}")
    except Exception as e:
        logging.error(f"[DISCORD] Erreur lors de l'ajout des rôles : {e}")

async def update_nickname(member: discord.Member, user: dict):
    first_name = user.get("firstName", "").strip()
    last_name = user.get("lastName", "").strip()
    new_nickname = f"{first_name} {last_name}".strip()

    if new_nickname and member.nick != new_nickname:
        try:
            await member.edit(nick=new_nickname)
            logging.info(f"[DISCORD] Pseudo mis à jour : {new_nickname}")
        except Exception as e:
            logging.warning(f"[DISCORD] Impossible de modifier le pseudo : {e}")
