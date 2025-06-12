# Projet Chatbot IA

Ce projet vise à construire un chatbot capable de répondre à des questions basées sur un ensemble de documents textuels (par exemple, des informations sur des champions de jeu, des objets, etc.).

Il utilise des techniques de traitement du langage naturel (NLP) pour comprendre et traiter les données textuelles :

- **Sentence Transformers** pour générer des embeddings (représentations vectorielles) des textes.
- **FAISS** pour créer un index efficace permettant une recherche rapide de similarité sémantique entre la question de l'utilisateur et les documents indexés.

L'objectif est de fournir des réponses pertinentes et rapides en trouvant les informations les plus similaires à la requête de l'utilisateur dans la base de connaissances.
