from flask import Flask, render_template, request
from kafka import KafkaProducer, KafkaConsumer
import json
import pandas as pd

app = Flask(__name__)

def get_movies_list():
    movies_df = pd.read_csv('hdfs:///projectdata/movies.dat', sep='::', header=None, engine='python', encoding='ISO-8859-1')
    movies_df.columns = ['movieId', 'title', 'genres']
    return movies_df[['movieId', 'title']].to_dict(orient='records')

def send_to_kafka(movie_id):
    try:
        producer = KafkaProducer(bootstrap_servers=['localhost:9092'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        data_to_send = {'movie_id': int(movie_id)}
        producer.send('selected_movie_topic', data_to_send)
        producer.flush()
        print(f"Sent to Kafka: {data_to_send}")
    except Exception as e:
        print(f"Error sending to Kafka: {e}")

def receive_from_kafka(movie_id):
    try:
        consumer = KafkaConsumer('recommendations_topic', group_id='movie_recommender_group', bootstrap_servers=['localhost:9092'], value_deserializer=lambda x: json.loads(x.decode('utf-8')), consumer_timeout_ms=30000)
        for message in consumer:
            if message.value.get('movie_id') == int(movie_id):
                print(f"Received from Kafka: {message.value}")
                return message.value
        print("No relevant message received from Kafka")
        return []
    except Exception as e:
        print(f"Error receiving from Kafka: {e}")
        return []

@app.route('/', methods=['GET'])
def index():
    movies_list = get_movies_list()
    return render_template('index.html', movies=movies_list)

@app.route('/recommend', methods=['POST'])
def recommend():
    movie_id = request.form.get('movie')
    if not movie_id:
        return render_template('index.html', movies=get_movies_list(), error="Please select a movie.")
    
    print(f"Movie ID received from form: {movie_id}")
    send_to_kafka(movie_id)
    data = receive_from_kafka(movie_id)
    recommendations = []
    if data and 'recommendations' in data:
        recommendations_ids = data['recommendations']
        movies_list = get_movies_list()
        # Convert movie IDs in movies_list to integers for comparison
        movies_dict = {int(movie['movieId']): movie for movie in movies_list}
        recommendations = [movies_dict[movie_id] for movie_id in recommendations_ids if movie_id in movies_dict]
    
    return render_template('index.html', movies=get_movies_list(), recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
