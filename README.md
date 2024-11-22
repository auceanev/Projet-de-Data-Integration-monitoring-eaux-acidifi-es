# Projet de Data Integration:Monitoring des eaux acidifiees

Ce projet vise à surveiller les niveaux chimiques dans les eaux acidifiées en temps réel avec Kafka, Spark et HDFS


## Description Générale



## Table des matières
1. [Description du projet](#description-du-projet)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Technologies utilisées](#technologies-utilisées)

## Installation

### Prérequis
Voici les logiciels nécessaires pour exécuter le projet.

- **Python 3.x**
- **Apache Kafka**
- **Apache Spark**
- **Hadoop HDFS**
- **PostgreSQL**

## Structure du Projet
- **kafka/** : Contient les scripts pour envoyer des données depuis Kafka.
- **spark/** : Scripts de traitement des données en temps réel avec Spark Streaming.
- **hdfs/** : Configuration et scripts pour le stockage dans HDFS.
- **dashboard/** : Configuration de la visualisation avec Grafana.


### Étapes d'installation
Les étapes pour installer votre projet localement.

1. Cloner le dépôt

```bash
git clone https://github.com/auceanev/Projet-de-Data-Integration-monitoring-eaux-acidifi-es.git

cd Projet-de-Data-Integration-monitoring-eaux-acidifi-es
```
2. Installer les dépendances

`pip install -r requirements.txt`

3. Lancer le producteur Kafka

## Instructions d'exécution
1. Démarrer Kafka et HDFS.
2. Lancer le producteur Kafka :
   ```bash
   python kafka_producer.py
```
3. Lancer le consommateur Spark :
   ```bash
   spark-submit spark_consumer.py

4. Utilisez la commande suivante pour créer le topic Kafka `water-quality` :
 ```bash
kafka-topics.sh --create --topic water-quality --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1


4. Visualiser les résultats sur Grafana.
## Introduction

Ce projet vise à construire un pipeline d’intégration de données en temps réel en utilisant Kafka pour le streaming, Spark pour le traitement des données, et HDFS pour le stockage. Les jeux de données suivants sont utilisés :

* LTM_Data_2022_8_1
* Methods_2022_8_1
* Site_Information_2022_8_1

# Objectifs:
1. Intégrer les données en provenance de fichiers et du streaming Kafka.
2. Joindre et enrichir les jeux de données pour produire des métriques utiles.
3. Assurer la traçabilité et la gestion des versions des données.
4. Mettre en place une architecture de stockage performante pour le traitement analytique.

## Étape 1 : Compréhension des Données
_Statut : FAIT_
Exploration initiale des jeux de données via une inspection manuelle et des outils comme Pandas et Spark.
Identification des colonnes clés :
* LTM_Data_2022_8_1 : Informations temporelles et mesures.
* Methods_2022_8_1 : Détails des méthodologies utilisées.
* Site_Information_2022_8_1 : Métadonnées sur les sites.
Relations principales définies :
site_id et method_id comme colonnes de jointure potentielles.


## Auteurs
- Votre Nom
