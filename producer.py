import time
from pymongo import MongoClient
import random
from azure.eventhub import EventHubProducerClient, EventData
import json
import os
from dotenv import load_dotenv

load_dotenv()


# CONFIGURATION
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("streamvault")

EVENTHUB_CONNECTION_STR = os.getenv("EVENTHUB_KEY")
def load_data_with_mongodb():
    try:
        client_mongo = MongoClient(MONGO_URI)
        db = client_mongo[DB_NAME]
       
        clients = list(db["clients"].find({},{"_id":1}))
        catalogue = list(db["catalogue"].find({}, {"_id": 1, "pagesNumber": 1}))

        client_mongo.close()
        return clients, catalogue
    except Exception as e:
        print(f"erreur de connexion a mongodb {e}")
        return [], []


load_data_with_mongodb()


def generer_commande(clients, catalogue):
    client_doc = random.choice(clients)
    item_doc = random.choice(catalogue)

    titre_id = item_doc["_id"]
    prix_fixe = round(random.uniform(5, 20), 2)

    return {
        "client_id": client_doc["_id"],
        "titre_id": titre_id,    
        "prix": prix_fixe,  
        "timestamp": time.time()
    }


def run():
    print("Connexion à MongoDB pour charger le catalogue et les clients...")
    clients, catalogue = load_data_with_mongodb()
    if not clients or not catalogue:
        print("Impossible de récupérer les données de MongoDB")
        return

    print(f"Chargé avec succès : {len(clients)} clients et {len(catalogue)} titres depuis MongoDB.")

    producer = EventHubProducerClient.from_connection_string(conn_str=EVENTHUB_CONNECTION_STR)
    print("Démarrage du producteur de commandes en temps réel")
    try:
        while True:
            cmd = generer_commande(clients, catalogue)
            batch = producer.create_batch()
            batch.add(EventData(json.dumps(cmd)))
            
            producer.send_batch(batch)
            print(f"Commande envoyée : {cmd}")
            
            time.sleep(3)
    except KeyboardInterrupt:
        print("Arrêt du producteur.")
    finally:
        producer.close()

if __name__ == '__main__':
    run()