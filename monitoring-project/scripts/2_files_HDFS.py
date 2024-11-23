import os
from pyspark.sql import SparkSession

# Spécifier le chemin de Java
os.environ["JAVA_HOME"] = "/path/to/java8"  # Remplace par le chemin correct
os.environ["PATH"] = os.environ["JAVA_HOME"] + "/bin:" + os.environ["PATH"]


# Créer une session Spark
spark = SparkSession.builder \
    .appName("DataIntegration") \
    .getOrCreate()

# Lire les fichiers depuis HDFS
methods_df = spark.read.csv("hdfs://Users/ines/Desktop/PROJET_DATA_INTEGRATION/Methods_2022_8_1.csv", header=True, inferSchema=True)
site_info_df = spark.read.csv("hdfs://Users/ines/Desktop/PROJET_DATA_INTEGRATION/Site_Information_2022_8_1.csv", header=True, inferSchema=True)

# Afficher les schémas
methods_df.printSchema()
site_info_df.printSchema()

