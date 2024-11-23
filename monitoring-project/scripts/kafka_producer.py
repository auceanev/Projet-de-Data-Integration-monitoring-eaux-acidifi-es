import six
import sys

if sys.version_info >= (3, 12, 0):
    sys.modules['kafka.vendor.six.moves'] = six.moves

import time
import pandas as pd
import json
from kafka import KafkaProducer
import logging

# Configurer le logger pour enregistrer les messages dans un fichier
logging.basicConfig(filename='producer_logs.txt', level=logging.INFO, format='[%(asctime)s] %(levelname)s - %(message)s')

logging.info("Kafka Producer démarré.")
logging.info("Lecture des données depuis LTM_Data_2022_8_1.xlsx.")


# Charger les données
data = pd.read_excel('/Users/ines/Desktop/PROJET_DATA_INTEGRATION/LTM_Data_2022_8_1.xlsx')

# Sélectionner les colonnes nécessaires
data = data[['SITE_ID', 'PH_LAB', 'WTEMP_DEG_C']]

# Configurer le Producer Kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Envoyer les données par lots de 10
batch_size = 10
for i in range(0, len(data), batch_size):
    batch = data[i:i+batch_size].to_dict(orient='records')
    for record in batch:
        producer.send('water-quality', record)
        print(f"Sent: {record}")  # Pour le débogage
    
    producer.flush()  # S'assurer que tous les messages sont envoyés
    print(f"Sent batch {i//batch_size + 1}")
    time.sleep(10)   

producer.close()
