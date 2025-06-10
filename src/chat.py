import json
import pickle
import numpy as np
import nltk
from nltk.stem import PorterStemmer
from tensorflow.keras.models import load_model
import random
import re
import requests

API_KEY = "RGAPI-e1336a1b-1cd6-4b0b-934d-1a479d0a359a"
REGION = "euw1"

stemmer = PorterStemmer()

with open('data/intents.json') as file:
    intents = json.load(file)

model = load_model('model/chatbot_model.h5')
words, labels,_= pickle.load(open("model/training_data.pkl", "rb"))

def extract_pseudo(input_text):
    text_lower = input_text.lower()
    prefixes = [
        "quel est le rang de",
        "donne-moi les infos sur",
        "je veux connaître le classement de",
        "peux-tu trouver le rang pour le pseudo",
        "infos joueur riot api pour",
        "pseudo et rang de",
        "le rang de",
        "infos sur",
        "classement de",
        "rang pour",
        "le pseudo de",
        "pour le pseudo",
        "le pseudo",
        "de", 
        "pour",
        "sur",
        "du joueur",
    ]
    extracted_name = ""
    
    for prefix in prefixes:
        trigger_phrase = prefix + " "
        if trigger_phrase in text_lower:
            start_index = text_lower.find(trigger_phrase) + len(trigger_phrase)
            potential_name = input_text[start_index:]
            
            potential_name = potential_name.strip()
            if potential_name.endswith("?"):
                potential_name = potential_name[:-1].strip()
            elif potential_name.endswith("."):
                potential_name = potential_name[:-1].strip()
            elif potential_name.endswith("!"):
                potential_name = potential_name[:-1].strip()
            
            if potential_name:
                extracted_name = potential_name
                break 

    return extracted_name

def get_summoner_info(summoner_name):
    url = f"https://{REGION}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
    headers = {"X-Riot-Token": API_KEY}
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Erreur {response.status_code} : {response.text}")
        return None
    
def bag_of_words(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [stemmer.stem(word) for word in sentence_words]
    bag = [1 if word in sentence_words else 0 for word in words]
    return np.array(bag)

def chat_response():
    print("LoLBot : Tape 'quit' pour quitter.")
    while True: 
        input_text = input("Toi : ")
        if input_text.lower() == 'quit':
            break
            
        bow = bag_of_words(input_text)
        res = model.predict(np.array([bow]))[0]
        idx = np.argmax(res)
        tag = labels[idx]

        confidence_threshold = 0.6 
        if res[idx] > confidence_threshold:
            if tag == "player_pseudo_rank":
                summoner_name = extract_pseudo(input_text)
                if summoner_name:
                    info = get_summoner_info(summoner_name)
                    for intent_obj in intents["intents"]:
                        if intent_obj["tag"] == tag:
                            print(f"LoLBot : {random.choice(intent_obj['responses'])}")
                            print(f"LoLBot : Voici les informations pour le joueur {summoner_name} :")
                            print(f"LoLBot : {info}")
                            break
                   
                else:
                    print("LoLBot : Je n'ai pas réussi à identifier le nom de l'invocateur. Pourriez-vous le formuler autrement ou le préciser ?")
            else:
            
                for intent_obj in intents["intents"]:
                    if intent_obj["tag"] == tag:
                        print(f"LoLBot : {random.choice(intent_obj['responses'])}")
                        break 
        else:
            print("LoLBot : Désolé, je ne comprends pas ta question...")

if __name__ == "__main__":
    chat_response()