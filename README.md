# Real-Time Movie Recommendation System - Project README


## Introduction
This project presents a real-time movie recommendation system using Apache Kafka for message handling, Apache Spark for processing large-scale data, and Flask for creating a web application interface. The system leverages collaborative filtering with the ALS (Alternating Least Squares) algorithm to provide movie recommendations based on user ratings.

## System Architecture
1. **Flask Web Application**: Serves as the user interface for selecting movies and displaying recommendations.
2. **Apache Kafka**: Acts as a messaging system between different components of the application.
3. **Spark ALS Model**: Utilizes Spark's machine learning library to generate movie recommendations.
4. **Spark Streaming**: Processes data in real-time to update recommendations based on user input.



## Setup and Installation

### Prerequisites
- Apache Hadoop
- Apache Spark (version 3.3.3 or higher)
- Apache Kafka
- Python 3
- Flask
- Pandas
- Kafka Python Package

### Installation Steps
1. **Install Hadoop, Spark, and Kafka**: Follow the official documentation for installation and setup.
2. **Run Hadoop, Spark, and Kafka Services**: Ensure all services are running correctly.
3. **Prepare Data**: Place the `movies.dat` and `ratings.dat` files in the HDFS (Hadoop Distributed File System).

### Running the Components
1. **Train the Recommendation Model**:
   ```bash
   /usr/local/spark-3.3.3-bin-hadoop3/bin/spark-submit ~/real-time-movie-recommendation/recommendation_model.py
   ```
   This script trains the ALS model and saves it for later use.

2. **Start the Spark Streaming Application**:
   ```bash
   /usr/local/spark-3.3.3-bin-hadoop3/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.3 ~/real-time-movie-recommendation/streaming_recommendation.py
   ```
   This application listens for new movie selections from the Kafka topic and processes recommendations in real-time.

3. **Run the Flask Web Application**:
   ```bash
   flask run
   ```
   Launches the web interface where users can select movies and view recommendations.

![image](https://github.com/Zakariaasr/movie-recommendation/assets/102974751/1ec6df1a-e3e4-46d3-9661-fd1f543d25d8)

## Usage
- Open the Flask web application.
- Select a movie from the dropdown list.
- The system will display recommended movies based on the selection.

## Components Overview
- `app.py`: The Flask application for the user interface.
- `model_recommendation.py`: Script to train the ALS recommendation model using Spark.
- `spark_streaming.py`: Spark Streaming application to process real-time data from Kafka and generate recommendations.

## Additional Information
- The system is designed for educational and demonstration purposes.
- Performance and scalability depend on the configuration of Apache Hadoop, Spark, and Kafka clusters.

## Contributions and Feedback
Contributions to this project are welcome. Please provide feedback and suggestions to improve the system's functionality and user experience.
