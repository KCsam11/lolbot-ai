import json

def format_champion(champ_data):
    name = champ_data["name"]
    title = champ_data["title"]
    tags = ", ".join(champ_data["tags"])
    blurb = champ_data["blurb"]
    stats = champ_data["stats"]
    info = champ_data["info"]
    partype = champ_data["partype"]

    return f"""{name} — {title}
Rôle : {tags}
Ressource : {partype}
Difficulté : {info['difficulty']}/10

Statistiques :
- PV : {stats['hp']} (+{stats['hpperlevel']}/niv)
- Attaque : {stats['attackdamage']} (+{stats['attackdamageperlevel']}/niv)
- Vitesse d’attaque : {stats['attackspeed']}
- Armure : {stats['armor']} (+{stats['armorperlevel']}/niv)
- Résistance magique : {stats['spellblock']} (+{stats['spellblockperlevel']}/niv)
- Vitesse de déplacement : {stats['movespeed']}

Résumé : {blurb}
""".strip()

def parse_all_champions(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    champions = data["data"]
    return [format_champion(champ) for champ in champions.values()]


if __name__ == "__main__":
    formatted = parse_all_champions("data/champions_summary_fr_FR.json")
    with open("data/champions_formatted.txt", "w", encoding="utf-8") as f:
          for champ in formatted:
            f.write(champ + "\n\n")
            