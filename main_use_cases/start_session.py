from pyspark.sql import SparkSession

#starting spark session
spark = SparkSession.builder \
    .master("local") \
    .appName("Use Cases") \
    .getOrCreate()