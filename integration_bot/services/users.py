import discord
from utils import slugify

async def assign_roles_to_member(member: discord.Member, teams: list):
    discord_id = str(member.id)
    guild = member.guild

    user_found = None
    team = None

    for t in teams:
        for user in t["users"]:
            if user["discordId"] == discord_id:
                user_found = user
                team = t
                break
        if user_found:
            break

    if not user_found:
        try:
            await member.send("Bienvenue ! Pour accéder aux rôles, synchronise ton compte ici : https://integration.utt.fr/sync")
        except Exception as e:
            print(f"[DISCORD] Erreur d'envoi du message privé : {e}")
        return

    roles_to_assign = []

    #Construction des noms de rôles selon la logique de setup_discord_structure
    team_name = team.get("name", "No name")
    faction_name = team.get("faction", "No faction")
    team_role_name = slugify(f"{team_name} - {faction_name}")
    faction_role_name = slugify(faction_name)

    team_role = discord.utils.get(guild.roles, name=team_role_name)
    faction_role = discord.utils.get(guild.roles, name=faction_role_name)

    if team_role:
        roles_to_assign.append(team_role)
    else:
        print(f"[DISCORD] Rôle d'équipe introuvable : {team_role_name}")

    if faction_role:
        roles_to_assign.append(faction_role)
    else:
        print(f"[DISCORD] Rôle de faction introuvable : {faction_role_name}")

    permission = user_found.get("permission")
    if permission == "Nouveau":
        new_role = discord.utils.get(guild.roles, name="Nouveau")
        if new_role:
            roles_to_assign.append(new_role)
    elif permission == "Student":
        leader_role = discord.utils.get(guild.roles, name="Chef d'équipe")
        if leader_role:
            roles_to_assign.append(leader_role)

    try:
        await member.add_roles(*roles_to_assign)
        print(f"[DISCORD] Rôles attribués à {member.display_name}: {[r.name for r in roles_to_assign]}")
    except Exception as e:
        print(f"[DISCORD] Erreur lors de l'ajout des rôles : {e}")

    # 🔤 Renommer le membre avec prénom + nom
    first_name = user_found.get("firstName", "").strip()
    last_name = user_found.get("lastName", "").strip()
    new_nickname = f"{first_name} {last_name}".strip()

    if new_nickname and member.nick != new_nickname:
        try:
            await member.edit(nick=new_nickname)
            print(f"[DISCORD] Pseudo mis à jour : {new_nickname}")
        except Exception as e:
            print(f"[DISCORD] Impossible de modifier le pseudo : {e}")
