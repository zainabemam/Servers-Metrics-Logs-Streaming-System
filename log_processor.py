# %%
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, window, regexp_extract, to_timestamp, when
from pyspark.sql.types import StringType

# %%

# Initialize Spark Session with Kafka package
spark = SparkSession.builder \
    .appName("LogProcessor") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.4") \
    .getOrCreate()

# %%
# Read from Kafka
df_raw = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "loadbalancer-logs") \
    .load()

# %%
# Decode the value
lines = df_raw.selectExpr("CAST(value AS STRING)")

# %%
# Regex parsing and initial transformation
parsed =lines.select(
    regexp_extract("value", r"^(\S+) - (\S+) \[(.*?)\] (GET|POST) (\S+) (\d{3}) (\d+)$", 1).alias("ip"),
    regexp_extract("value", r"^(\S+) - (\S+) \[(.*?)\] (GET|POST) (\S+) (\d{3}) (\d+)$", 3).alias("timestamp"),
    regexp_extract("value", r"^(\S+) - (\S+) \[(.*?)\] (GET|POST) (\S+) (\d{3}) (\d+)$", 4).alias("method"),
    regexp_extract("value", r"^(\S+) - (\S+) \[(.*?)\] (GET|POST) (\S+) (\d{3}) (\d+)$", 6).cast("int").alias("status")
)

# %%
# Convert timestamp string to actual timestamp
parsed = parsed.withColumn("event_time", to_timestamp("timestamp", "dd MMM yyyy HH:mm:ss z"))



# %%
# Add success/failure columns
parsed = parsed.withColumn("success", (col("status") < 400).cast("int"))
parsed = parsed.withColumn("failed", (col("status") >= 400).cast("int"))

# %%
windowed = parsed \
    .withWatermark("event_time", "10 minutes") \
    .groupBy(
        window(col("event_time"), "5 minutes"),
        col("method"),
        col("success")
    ) \
    .count()

# %%
query = windowed.writeStream \
    .outputMode("append") \
    .format("parquet") \
    .option("path", "file:///tmp/log_summary/") \
    .option("checkpointLocation", "file:///tmp/log_checkpoint/") \
    .trigger(once=True) \
    .start()

query.awaitTermination()



