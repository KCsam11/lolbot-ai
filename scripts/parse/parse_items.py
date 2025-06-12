import json

def format_items(item_data):
   
    name = item_data["name"]
    description = item_data["description"]
    plaintext = item_data.get("plaintext", "")
    gold = item_data["gold"]["total"]
    tags = ", ".join(item_data["tags"])
    
    cleaned_description = description.replace('<br>', '\n').replace('<li>', '- ').replace('</li>', '').replace('<ul>', '').replace('</ul>', '')
    import re
    cleaned_description = re.sub(r'<[^>]+>', '', cleaned_description)
    cleaned_description = cleaned_description.strip()
    
    return f"""Nom de l'objet : {name}
-----------------------------------
Description :
{cleaned_description}

Effet simple (si disponible) :
{plaintext}

Prix total : {gold} pièces d’or
Catégories : {tags}
""".strip()


def parse_all_items(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    items = data["data"]
    return [format_items(item) for item in items.values()]

if __name__ == "__main__":
    formatted_items = parse_all_items("data/items_fr_FR.json")
    with open("data/items_formatted.txt", "w", encoding="utf-8") as f:
        for item in formatted_items:
            f.write(item + "\n\n")