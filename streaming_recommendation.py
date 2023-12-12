from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALSModel
from pyspark.sql.functions import col, lit, udf
from pyspark.sql.types import StringType, IntegerType
from kafka import KafkaProducer
import json

# Define a UDF to parse the JSON string and extract the movie_id
def parse_movie_id(json_str):
    try:
        return json.loads(json_str)["movie_id"]
    except json.JSONDecodeError:
        return None

parse_movie_id_udf = udf(parse_movie_id, StringType())

def send_recommendations_to_kafka(movie_id, recommendations):
    try:
        producer = KafkaProducer(bootstrap_servers="localhost:9092", value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        producer.send("recommendations_topic", {'movie_id': movie_id, 'recommendations': recommendations})
        producer.flush()
    except Exception as e:
        print(f"Error sending recommendations to Kafka: {e}")

def process_batch(df, epoch_id):
    try:
        if df.count() > 0:
            print(f"Processing batch with {df.count()} rows.")

            # Parse the movie ID from the incoming data
            df = df.withColumn("movieIdStr", col("value"))
            df = df.withColumn("movieId", parse_movie_id_udf(col("movieIdStr")).cast(IntegerType()))

            # Generate recommendations for each movie ID in the batch
            for row in df.collect():
                movie_id = row.movieId
                movie_recommendations = model.recommendForItemSubset(df.select("movieId").distinct(), 5)

                # Extract user recommendations for the movie
                recs = [r.userId for r in movie_recommendations.collect()[0]['recommendations']]
                send_recommendations_to_kafka(movie_id, recs)
    except Exception as e:
        print(f"Error in process_batch: {e}")

# Initialize the Spark session and load the model
spark = SparkSession.builder.appName("StreamingMovieRecommendations").getOrCreate()
model = ALSModel.load("hdfs:///projectdata/als_model")

# Read from Kafka topic
kafka_df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "selected_movie_topic") \
    .load() \
    .selectExpr("CAST(value AS STRING)")

# Start the streaming query
query = kafka_df.writeStream.foreachBatch(process_batch).start()
query.awaitTermination()
