import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, when, lit, isnan
from pyspark.sql.types import StructType, StructField, StringType, FloatType
import psycopg2
import json

# Configuration de l'environnement
os.environ['JAVA_HOME'] = '/opt/homebrew/opt/openjdk@11/libexec/openjdk.jdk/Contents/Home'
os.environ['PATH'] = os.environ['JAVA_HOME'] + '/bin:' + os.environ['PATH']
os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.4 pyspark-shell'

# Fonction pour tester la connexion PostgreSQL
def test_postgres_connection():
    try:
        conn = psycopg2.connect(
            dbname="base_donnees",
            user="inesines",
            password="inesines",
            host="localhost",
            port="5432"
        )
        print("Connexion réussie à PostgreSQL")
        conn.close()
    except Exception as e:
        print(f"Erreur de connexion à PostgreSQL : {str(e)}")

# Tester la connexion avant de commencer
test_postgres_connection()

# Créer une session Spark
spark = SparkSession.builder \
    .appName("WaterQualityStreaming") \
    .getOrCreate()

# Définir le schéma des données
schema = StructType([
    StructField("SITE_ID", StringType(), True),
    StructField("PH_LAB", FloatType(), True),
    StructField("WTEMP_DEG_C", FloatType(), True)
])

# Lire les données de Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "water-quality") \
    .load()

# Convertir les données en JSON et appliquer le schéma
parsed_df = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")) \
    .select("data.*")

# Nettoyage des données
cleaned_df = parsed_df.select(
    col("SITE_ID"),
    when(col("PH_LAB").isNull() | isnan(col("PH_LAB")), lit(None)).otherwise(col("PH_LAB")).alias("PH_LAB"),
    when(col("WTEMP_DEG_C").isNull() | isnan(col("WTEMP_DEG_C")), lit(None)).otherwise(col("WTEMP_DEG_C")).alias("WTEMP_DEG_C")
)

def write_to_postgres(batch_df, batch_id):
    print(f"Démarrage de write_to_postgres pour le batch {batch_id}")
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(
            dbname="base_donnees",
            user="inesines",
            password="inesines",
            host="localhost",
            port="5432"
        )
        cur = conn.cursor()
        
        for row in batch_df.collect():
            site_id = row['SITE_ID'] if row['SITE_ID'] else None
            ph_lab = row['PH_LAB'] if row['PH_LAB'] is not None else None
            wtemp_deg_c = row['WTEMP_DEG_C'] if row['WTEMP_DEG_C'] is not None else None
            
            print(f"Tentative d'insertion : site_id={site_id}, ph_lab={ph_lab}, wtemp_deg_c={wtemp_deg_c}")
            
            cur.execute(
                "INSERT INTO water_quality (site_id, ph_lab, wtemp_deg_c) VALUES (%s, %s, %s)",
                (site_id, ph_lab, wtemp_deg_c)
            )
            print(f"Insertion réussie : site_id={site_id}, ph_lab={ph_lab}, wtemp_deg_c={wtemp_deg_c}")

        # Valider les transactions après toutes les insertions
        conn.commit()
        print(f"Batch {batch_id} traité avec succès")
    except Exception as e:
        print(f"Erreur inattendue dans le batch {batch_id} : {str(e)}")
        if conn:
            conn.rollback()  # Annuler les modifications en cas d'erreur
    finally:
        if cur:
            cur.close()  # Fermer le curseur si il a été créé
        if conn:
            conn.close()  # Fermer la connexion si elle a été établie
    print(f"Fin de write_to_postgres pour le batch {batch_id}")

# Fonction pour traiter chaque batch
def process_batch(batch_df, batch_id):
    print(f"Traitement du batch {batch_id}")
    print("Contenu du batch :")
    batch_df.show(truncate=False)
    print("Schéma du batch :")
    batch_df.printSchema()
    write_to_postgres(batch_df, batch_id)

# Écrire les données dans PostgreSQL et afficher dans la console
query = cleaned_df.writeStream \
    .trigger(processingTime='10 seconds') \
    .foreachBatch(process_batch) \
    .outputMode("append") \
    .start()

# Attendre la terminaison du query
query.awaitTermination()
