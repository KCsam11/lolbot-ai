import json
import re
import os
def clean_html(raw_html: str) -> str:
    if not raw_html:
        return ""
    text = raw_html.replace('<br>', '\n').replace('<br />', '\n')
    clean_text = re.sub(r'<[^>]+>', '', text)
    return clean_text.strip()


def format_detail_champion(champion_data: dict) -> dict:
    formatted_champion = {}
    formatted_champion['name'] = champion_data.get('name', 'N/A')
    formatted_champion['title'] = champion_data.get('title', 'N/A')

    #Skin
    skins = champion_data.get('skins', [])
    formatted_champion['skins'] = [skin.get('name', 'N/A') for skin in skins if skin]

    #Lore
    formatted_champion['lore'] = champion_data.get('lore', 'Lore non disponible.')

    # Allytips (conseils pour jouer avec)
    formatted_champion['allytips'] = champion_data.get('allytips', ['Aucun conseil allié disponible.'])

    # Enemytips (conseils pour jouer contre)
    formatted_champion['enemytips'] = champion_data.get('enemytips', ['Aucun conseil ennemi disponible.'])
    
    #Spells
    spells_data = champion_data.get('spells', [])
    formatted_spells = []
    for spell in spells_data:
        if spell:
            formatted_spell = {
                'name': spell.get('name', 'N/A'),
                'description': clean_html(spell.get('description', 'Description non disponible.')),
                'tooltip': clean_html(spell.get('tooltip', 'Tooltip non disponible.'))
            }
            formatted_spells.append(formatted_spell)
    formatted_champion['spells'] = formatted_spells
   
    # Passive
    passive_data = champion_data.get('passive')
    if passive_data:
        formatted_champion['passive'] = {
            'name': passive_data.get('name', 'N/A'),
            'description': clean_html(passive_data.get('description', 'Description non disponible.'))
        }
    else:
        formatted_champion['passive'] = {
            'name': 'N/A',
            'description': 'Passif non disponible.'
        }

    # Préparation des chaînes pour la f-string finale
    name_str = formatted_champion['name']
    title_str = formatted_champion['title']
    lore_str = formatted_champion['lore']
    
    skins_items_str = "\n".join([f"    - {skin_name}" for skin_name in formatted_champion['skins']])
    allytips_items_str = "\n".join([f"    - {tip}" for tip in formatted_champion['allytips']])
    enemytips_items_str = "\n".join([f"    - {tip}" for tip in formatted_champion['enemytips']])

    # Formatage des Compétences (Spells)
    if formatted_champion['spells']:
        spells_items_str = "\n".join([f"    - {s['name']}: {s['description']}" for s in formatted_champion['spells']])
    else:
        spells_items_str = "    - Aucune compétence disponible."

    passive_item_str = f"    - {formatted_champion['passive']['name']}: {formatted_champion['passive']['description']}"

    return f"""{name_str} — {title_str}

Lore:
{lore_str}

Skins:
{skins_items_str}

Alliés:
{allytips_items_str}

Ennemis:
{enemytips_items_str}

Compétences:
{spells_items_str}

Passif:
{passive_item_str}
""".strip()


def parse_detail_champion(directory_path: str) -> list[dict]:
    all_formatted_champions = []
    if not os.path.isdir(directory_path):
        print(f"Error: Provided path '{directory_path}' is not a directory.")
        return all_formatted_champions

    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):  # Assuming champion files are .json
            file_path = os.path.join(directory_path, filename)
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                formatted_champion = format_detail_champion(data)
                all_formatted_champions.append(formatted_champion)
            except json.JSONDecodeError:
                print(f"Warning: Could not decode JSON from file {file_path}")
            except Exception as e:
                print(f"Warning: Error processing file {file_path}: {e}")
    return all_formatted_champions


if __name__ == "__main__":
    all_champions_data = parse_detail_champion("data/champions_details_fr_FR")
    with open("data/detail_champions_formatted.txt", "w", encoding="utf-8") as f:
        if not all_champions_data:
            f.write("No champion data found or processed.\n") 
        else:
            for champ_data in all_champions_data: # champ_data is a dictionary
                f.write(champ_data + "\n\n") # Separator for readability