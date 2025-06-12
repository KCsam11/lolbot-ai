import requests
import json
import os
from tqdm import tqdm

# Fonction pour récupérer les données depuis l'API Riot
def fetch_data_from_riot_api(api_key, region, api_endpoint):
    headers = {
        "X-Riot-Token": api_key,
    }
    try: 
        if "ddragon.leagueoflegends.com" in api_endpoint:
            response = requests.get(api_endpoint, timeout=10)
        else:
            response = requests.get(api_endpoint, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête à l'API Riot ({api_endpoint}): {e}")
        return None
    except Exception as e :
        print(f"Erreur inattendue ({api_endpoint}): {e}")
        return None

# Récupération et sauvegarde des données  
def recupData(api_data, file_path, name_for_log):
    if api_data:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as file: # Ajout de encoding='utf-8'
            json.dump(api_data, file, indent=4, ensure_ascii=False) # Ajout de ensure_ascii=False pour les caractères spéciaux
    else:
        print(f"Échec de la récupération des données des {name_for_log}.")
    

# Fonction principale pour exécuter le script
if __name__ == "__main__":
    api_key = "RGAPI-e1336a1b-1cd6-4b0b-934d-1a479d0a359a"
    region = "euw1"
    lol_version = "15.11.1"
    language = "fr_FR"

    if not os.path.exists('data'):
        os.makedirs('data')

    # Récupération des données des champions
    all_champions_list_endpoint = f"https://ddragon.leagueoflegends.com/cdn/{lol_version}/data/{language}/champion.json"
    print(f"\nRécupération de la liste générale des champions depuis {all_champions_list_endpoint}...")

    champions_summary_data = fetch_data_from_riot_api(api_key, region, all_champions_list_endpoint)

    if champions_summary_data and 'data' in champions_summary_data:
        recupData(champions_summary_data, f'data/champions_summary_{language}.json', "liste générale des champions")
        champions_dict = champions_summary_data['data']
        print(f"\nTrouvé {len(champions_dict)} champions. Récupération des détails pour chacun...")

        champions_details_folder = f'data/champions_details_{language}'
        if not os.path.exists(champions_details_folder):
            os.makedirs(champions_details_folder)
        
        print(f"\nTraitement des {len(champions_dict)} champions:")
        for champion_id, champion_info in tqdm(champions_dict.items(), desc="Champions", unit="champion"):
            champion_name = champion_info['name']
            champion_detail_endpoint = f"https://ddragon.leagueoflegends.com/cdn/{lol_version}/data/{language}/champion/{champion_id}.json"
            detailed_champion_data = fetch_data_from_riot_api(api_key, region, champion_detail_endpoint)

            if detailed_champion_data:
                if 'data' in detailed_champion_data and champion_id in detailed_champion_data['data']:
                    actual_data_to_save = detailed_champion_data['data'][champion_id]
                    file_path = os.path.join(champions_details_folder, f"{champion_id}.json")
                    recupData(actual_data_to_save, file_path, f"détails de {champion_name}")
                else:
                    tqdm.write(f"Structure de données inattendue pour {champion_name}. Données brutes sauvegardées.")
                    file_path = os.path.join(champions_details_folder, f"{champion_id}_raw.json")
                    recupData(detailed_champion_data, file_path, f"données brutes de {champion_name}")
            else:
                tqdm.write(f"Échec de la récupération des détails pour {champion_name}.")
    else:
        print("Échec de la récupération de la liste générale des champions. Impossible de continuer.")

    
    # Récupération des données des objets
    items_filename  = f'items_{language}.json'
    items_file_path = os.path.join("data", items_filename)

    items_endpoint = f"https://ddragon.leagueoflegends.com/cdn/{lol_version}/data/{language}/item.json"
    item_data = fetch_data_from_riot_api(api_key, region, items_endpoint)

    print(f"\nTraitement des items:")

    with tqdm(total=1, desc="Items", unit="fichier") as pbar:
            items_data = fetch_data_from_riot_api(api_key, region, items_endpoint)
            pbar.update(1) # Met à jour la barre une fois l'opération terminée
        
    if items_data:
        recupData(items_data, items_file_path, "items")
        tqdm.write(f"Données des items enregistrées dans '{items_file_path}'.")

    else:
        tqdm.write("Échec de la récupération des données des items.")

    