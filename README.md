# Projet de Data Integration: Monitoring des eaux acidifiees

Ce projet vise à surveiller les niveaux chimiques dans les eaux acidifiées en temps réel avec Kafka, Spark et HDFS

## Table des matières
1. [Description du projet](#description-du-projet)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Technologies utilisées](#technologies-utilisées)

## Description Générale
Ce projet implémente un pipeline de traitement de données en temps réel utilisant Kafka et Spark. L'objectif est de consommer des données issues d'un fichier Excel, de les publier sur un topic Kafka, puis de les traiter en temps réel avec Spark Streaming. Les données sont ensuite intégrées et préparées pour des analyses futures.

## Installation

### Prérequis
Voici les logiciels nécessaires pour exécuter le projet.

- **Python 3.x**
- **Apache Kafka**
- **Apache Spark**
- **Hadoop HDFS**
- **PostgreSQL**

## Structure du Projet
- **kafka** : Contient les scripts pour envoyer des données depuis Kafka.
- **spark** : Scripts de traitement des données en temps réel avec Spark Streaming.
- **hdfs** : Configuration et scripts pour le stockage dans HDFS.

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
```

4. Utilisez la commande suivante pour créer le topic Kafka `water-quality` :
 ```bash
kafka-topics.sh --create --topic water-quality --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
```


# Objectifs:
1. Intégrer les données en provenance de fichiers et du streaming Kafka.
2. Joindre et enrichir les jeux de données pour produire des métriques utiles.
3. Assurer la traçabilité et la gestion des versions des données.
4. Mettre en place une architecture de stockage performante pour le traitement analytique.

## Étape I : Compréhension des Données
_Statut : FAIT_

Exploration initiale des jeux de données via une inspection manuelle et des outils comme Pandas et Spark.
Identification des colonnes clés :

* LTM_Data_2022_8_1 : Informations temporelles et mesures.
* Methods_2022_8_1 : Détails des méthodologies utilisées.
* Site_Information_2022_8_1 : Métadonnées sur les sites.

Relations principales définies :
site_id et method_id comme colonnes de jointure potentielles.

## Étapes II : Streaming Kafka

_Simulation du streaming Kafka : FAIT_
* Création d’un producteur Kafka qui :
	* Charge le fichier LTM_Data_2022_8_1.
	* Émet des lots de 100 lignes à un sujet Kafka spécifique (water-quality).
	* Implémente une pause de 10 secondes entre les lots.
	* Script testé avec un cluster Kafka local.
	
* Lecture des fichiers HDFS : Ne fonctionne pas (Cf HDFS.py)
* À développer : un script Spark capable de lire les fichiers Methods et Site_Informationdepuis HDFS.
* Utiliser SparkContext pour connecter HDFS et charger les données dans des DataFrames avec schéma défini.
 
## Étapes III : Consumer Kafka + Intégration des Données
_Statut : PARTIELLEMENT FAIT_

Consumer Kafka : FAIT
* Développement d’un Consumer Kafka basé sur Spark Streaming.
* Les données consommées sont converties en DataFrames Spark pour traitement ultérieur.
* Intégration dans le système : NON FAIT
* Intégrer chaque lot reçu dans un jeu de données principal.
* Implémenter la gestion des versions en enregistrant chaque lot traité avec un ID unique dans une table ou un répertoire dédié.
* Ajouter des métadonnées par lot (horodatage, numéro de version, taille) pour permettre des capacités de restauration en cas d’incohérence.
* Gestion des incohérences : NON FAIT
* Développer une procédure pour isoler les lots défectueux et retraiter le dernier lot traité avec succès.

## Étapes IV : Jointure et Enrichissement des Données
_Statut : NON FAIT_

* Identifier les champs correspondants (site_id, method_id) pour effectuer les jointures nécessaires entre les trois jeux de données.
* Définir les métriques à calculer, comme la moyenne des mesures par site ou par méthode, ou encore la distribution des données selon les catégories.

## Étapes V : Architecture de Stockage

Approche hybride que nous suggérons:

* HDFS pour stocker les données brutes et archivées.
* PostgreSQL comme base de données relationnelle pour stocker les métriques calculées et permettre des requêtes OLAP.
* Gestion des versions implémentée via une table PostgreSQL dédiée.

## Étapes VI : Documentation
_Statut : PARTIELLEMENT FAIT_

__Pipeline :__
	
Schéma général du pipeline (Kafka Producer → Kafka Consumer → Spark Processing → PostgreSQL).
*	Configuration de Kafka :
	*	Topics : water-quality.
	*	Brokers et paramètres du cluster Kafka.

__Procédure de récupération :__
	
	*	Étapes pour identifier et retraiter un lot défectueux.
	*	Commandes pour restaurer une version précédente des données.


Ce qu’on aurait aimé ajouter en plus:
	*	Ajouter des exemples concrets pour configurer le cluster Kafka et exécuter le consommateur et le producteur.”
	*	Inclure une section sur l’intégration de Spark avec PostgreSQL pour enregistrer les métriques calculées.
	*	Fournir des commandes ou scripts pour effectuer des requêtes sur les données enrichies.


Décisions Techniques
Choix de la Base de Données
	*	PostgreSQL : Sélectionné car plus fiable , voire tenace et ses capacités OLAP.
	*	HDFS : Utilisé pour le stockage des fichiers bruts.
Technologies Utilisées
	*	Apache Kafka : Streaming en temps réel.
	*	Apache Spark : Traitement de données distribuées.
	*	PostgreSQL : Stockage et requêtes analytiques.
	*	HDFS : Stockage distribué.
 
Nos Points Restants
	1.	Implémenter la lecture des fichiers depuis HDFS.
	2.	Finaliser l’intégration des données avec gestion des versions.
	3.	Ajouter la logique de gestion des incohérences dans le pipeline.
	4.	Effectuer les jointures des jeux de données et enrichir les données.
	5.	Étendre la documentation technique pour inclure des exemples pratiques et des guides étape par étape.



## Auteurs

- Sekari_ines - Titot_auceane - Nkuida_malaika - Demanou_lena
