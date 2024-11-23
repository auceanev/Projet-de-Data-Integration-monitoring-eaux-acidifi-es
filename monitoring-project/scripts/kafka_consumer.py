import os
os.environ['JAVA_HOME'] = '/opt/homebrew/opt/openjdk@11/libexec/openjdk.jdk/Contents/Home'
os.environ['PATH'] = os.environ['JAVA_HOME'] + '/bin:' + os.environ['PATH']

from confluent_kafka import Consumer, KafkaError
import json

# Configuration du consommateur
conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'my-group',
    'auto.offset.reset': 'earliest'
}

# Créer un consommateur Kafka
consumer = Consumer(conf)

# S'abonner au topic
consumer.subscribe(['water-quality'])

# Consommer les messages
try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print("Reached end of partition")
                continue
            else:
                print(f"Error: {msg.error()}")
                continue

        try:
            data = json.loads(msg.value().decode('utf-8'))
            print("Received data:")
            print(json.dumps(data, indent=2))  # Afficher les données de manière formatée

            # Vérifier si toutes les clés nécessaires sont présentes
            required_keys = ['SITE_ID', 'PH_LAB', 'WTEMP_DEG_C']
            if all(key in data for key in required_keys):
                print(f"Site ID: {data['SITE_ID']}, "
                      f"pH: {data['PH_LAB']}, "
                      f"Température de l'eau: {data['WTEMP_DEG_C']}°C")
            else:
                print("Warning: Some required keys are missing in the data")

        except json.JSONDecodeError:
            print(f"Error decoding JSON: {msg.value().decode('utf-8')}")
        except KeyError as e:
            print(f"KeyError: {e} is missing in the data")
        
        print("---")  # Séparateur entre les messages

except KeyboardInterrupt:
    print("Interrupted by user")
finally:
    consumer.close()
    print("Consumer closed")
