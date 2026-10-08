StreamVault

Projet Python permettant de récupérer des données depuis MongoDB et de les envoyer vers Azure Event Hubs.

Prérequis

Avant de commencer, installer :

Python 3.10 ou supérieur
MongoDB
Un compte Azure avec un Event Hub configuré
pip
Structure du projet
streamvault/
│
├── .env
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
│
└── main.py

Configuration des variables d'environnement

Copier le fichier .env.example vers .env.

Windows
copy .env.example .env

Linux / macOS
cp .env.example .env

Modifier ensuite le fichier .env avec les vraies valeurs :

MONGO_URI=mongodb://localhost:27017/
DB_NAME=streamvault

EVENTHUB_KEY="Endpoint=sb://your-eventhub.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=YOUR_SECRET_KEY;EntityPath=your-eventhub-name"

Le fichier .env contient des informations sensibles. Il ne doit pas être envoyé sur Git.

Fichier .gitignore

Le fichier .gitignore doit contenir :

.env

**pycache**/
\*.py[cod]

venv/
.venv/

.vscode/
.idea/

.DS_Store
Thumbs.db

Création de l'environnement virtuel
Windows
python -m venv venv
venv\Scripts\activate

Linux / macOS
python3 -m venv venv
source venv/bin/activate

Installation des dépendances

Installer les dépendances :

pip install -r requirements.txt

Si le fichier requirements.txt n'existe pas :

pip install pymongo azure-eventhub python-dotenv

Puis générer le fichier :

pip freeze > requirements.txt

Fichier requirements.txt

Les principales dépendances sont :

azure-eventhub
pymongo
python-dotenv

Chargement des variables d'environnement

Dans Python :

import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
EVENTHUB_CONNECTION_STR = os.getenv("EVENTHUB_KEY")

La variable EVENTHUB_KEY contient ici la connection string complète d'Azure Event Hubs.

Connexion à MongoDB

Exemple :

from pymongo import MongoClient

client = MongoClient(MONGO_URI)

db = client[DB_NAME]

print("Connexion MongoDB réussie")

Connexion à Azure Event Hubs

Exemple :

from azure.eventhub import EventHubProducerClient

producer = EventHubProducerClient.from_connection_string(
conn_str=EVENTHUB_CONNECTION_STR
)

print("Connexion Event Hub configurée")

Envoi d'un événement

Exemple :

import json
from azure.eventhub import EventHubProducerClient, EventData

producer = EventHubProducerClient.from_connection_string(
conn_str=EVENTHUB_CONNECTION_STR
)

event = {
"commande_id": 123,
"produit": "Produit A",
"quantite": 2
}

event_data = EventData(json.dumps(event))

with producer:
event_batch = producer.create_batch()
event_batch.add(event_data)
producer.send_batch(event_batch)

print("Événement envoyé avec succès")

Lancer le projet

Activer l'environnement virtuel puis lancer :

python main.py

Si le fichier principal s'appelle producer.py :

python producer.py

Tester les variables d'environnement

Pour vérifier que le fichier .env est correctement chargé :

import os
from dotenv import load_dotenv

load_dotenv()

print("MongoDB :", os.getenv("MONGO_URI"))
print("Database :", os.getenv("DB_NAME"))
print("Event Hub configuré :", bool(os.getenv("EVENTHUB_KEY")))

Résultat attendu :

MongoDB : mongodb://localhost:27017/
Database : streamvault
Event Hub configuré : True

Ne pas afficher directement la connection string dans les logs.

Dépannage
ModuleNotFoundError: No module named 'dotenv'

Installer :

pip install python-dotenv

ModuleNotFoundError: No module named 'azure'

Installer :

pip install azure-eventhub

ModuleNotFoundError: No module named 'pymongo'

Installer :

pip install pymongo

EVENTHUB_KEY vaut None

Vérifier :

Que le fichier .env existe.
Que .env est dans le dossier du projet.
Que load_dotenv() est appelé.
Que le nom de variable est exactement :
EVENTHUB_KEY=...

Que Python est lancé depuis le bon dossier.
Sécurité

Ne jamais mettre une vraie clé Azure directement dans le code.

Incorrect :

EVENTHUB_CONNECTION_STR = "Endpoint=sb://...SharedAccessKey=..."

Correct :

EVENTHUB_CONNECTION_STR = os.getenv("EVENTHUB_KEY")

Le fichier .env doit rester local et être exclu de Git.

Si une clé Azure a été publiée accidentellement, elle doit être révoquée ou régénérée dans Azure.

Commandes principales

Créer l'environnement virtuel :

python -m venv venv

Windows :

venv\Scripts\activate

Linux / macOS :

source venv/bin/activate

Installer les dépendances :

pip install -r requirements.txt

Lancer le projet :

python main.py

Résumé
.env.example
|
| copier
v
.env
|
| load_dotenv()
v
Python
|
+-- MONGO_URI
+-- DB_NAME
|
+-- EVENTHUB_KEY
|
v
Azure Event Hubs
