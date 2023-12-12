from pyspark.sql import SparkSession
from pyspark.ml.recommendation import ALS
from pyspark.sql.functions import col

# Initialize the Spark session
spark = SparkSession.builder.appName("ALSModel").getOrCreate()

# Load the data
ratings_data = spark.read.csv("hdfs:///projectdata/ratings.dat", sep="::", header=False, inferSchema=True)
ratings_data = ratings_data.withColumnRenamed("_c0", "userId") \
                           .withColumnRenamed("_c1", "movieId") \
                           .withColumnRenamed("_c2", "rating") \
                           .withColumnRenamed("_c3", "timestamp")

# Create and fit the ALS model
als = ALS(maxIter=5, regParam=0.01, userCol="userId", itemCol="movieId", ratingCol="rating")
model = als.fit(ratings_data)

# Save the model to a local directory
model_path = "hdfs:///projectdata/als_model"  # Replace with your desired local path
model.write().overwrite().save(model_path)

# Stop the Spark session
spark.stop()
