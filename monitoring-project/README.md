# Projet d'Intégration de Données - Streaming en Temps Réel avec Kafka et Spark

## Instructions pour Exécuter les Scripts

## Exécution du Projet
1. Démarrer Kafka.
2. Lancer le producteur pour envoyer les données vers Kafka.
3. Exécuter Spark Streaming pour traiter les données en continu.

## Description Générale
* Kafka Producer envoie des données vers le topic water-quality.
* Kafka Consumer reçoit ces données, les transforme en DataFrames via Spark Streaming.
* HDFS est utilisé pour le stockage des données en grandes quantités, permettant une gestion efficace et évolutive.
* Spark effectue les calculs des métriques et les stocke dans un format structuré.

## Instructions d'exécution

### 1. Démarrage des Services

1.1 Démarrez ZooKeeper

 ```
  /opt/kafka/bin/zookeeper-server-start.sh /opt/kafka/config/zookeeper.properties
```

	1.2 Démarrez Kafka

 ```
 /opt/kafka/bin/kafka-server-start.sh /opt/kafka/config/server.properties
```
### 2. Création des Topics Kafka

Utilisez la commande suivante pour créer le topic Kafka `water-quality` :
 ```
kafka-topics.sh --create --topic water-quality --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
```
### 3. Écriture et Consommation de Données

	3.1 Écrire le script pour envoyer des données au topic Kafka
cf producer.py

	2. Lancer le producer Kafka :
```
   python producer.py
```

6. Écrire le script pour consommer les données du topic et les traiter avec Spark
cf spark_streaming.py

3. Lancer le consommateur Spark :
 ```
   spark-submit spark_consumer.py
```


### 4. Enrichissement des Données


1. Lire les fichiers depuis HDFS
```
methods_df = spark.read.csv("hdfs://Users/ines/Desktop/PROJET_DATA_INTEGRATION/Methods_2022_8_1.csv", header=True, inferSchema=True)
site_info_df = spark.read.csv("hdfs://Users/ines/Desktop/PROJET_DATA_INTEGRATION/Site_Information_2022_8_1.csv", header=True, inferSchema=True)
```

2.joignez les données avec les flux Kafka
```
enriched_df = kafka_stream_df.join(methods_df, "common_column").join(site_info_df, "common_column")
```


3.Calcul des métriques
```
enriched_df.groupBy("region").avg("chemical_level").show()
```

### 5. Stockage des Données dans une Base de Données

1.Configurez PostgreSQL
```
sudo -u postgres createdb monitoring
```

2.Écrivez les données enrichies dans PostgreSQL

```
enriched_df.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/monitoring") \
    .option("dbtable", "enriched_data") \
    .option("user", "your_user") \
    .option("password", "your_password") \
    .save()

```
