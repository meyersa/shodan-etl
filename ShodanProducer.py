# Connects to the Shodan API and sends new information to Kafka 
# Should run in a loop 

# Sample generated by ChatGPT

import os
import requests
from kafka import KafkaProducer
import time

# Function to get Kafka connection details from environment variables
def get_kafka_connection_details():
    kafka_bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    kafka_topic = os.getenv("KAFKA_TOPIC")
    return kafka_bootstrap_servers, kafka_topic

# Function to produce message to Kafka topic
def produce_message(bootstrap_servers, topic, message):
    producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
    producer.send(topic, message.encode())
    producer.flush()

# Function to search Shodan API and send results to Kafka
def search_shodan_and_send(bootstrap_servers, topic, query, api_key):
    url = f"https://api.shodan.io/shodan/host/search?key={api_key}&query={query}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        for result in data['matches']:
            produce_message(bootstrap_servers, topic, str(result))
        print("Messages sent to Kafka successfully!")
    else:
        print("Error:", response.status_code)

if __name__ == "__main__":
    # Get Kafka connection details
    bootstrap_servers, topic = get_kafka_connection_details()

    # Get Shodan API key from environment variable
    api_key = os.getenv("SHODAN_API_KEY")

    if bootstrap_servers and topic and api_key:
        print("Using Kafka bootstrap servers:", bootstrap_servers)
        print("Using Kafka topic:", topic)
        print("Using Shodan API key:", api_key)

        # Define the search query for Shodan
        query = "apache"  # Change this to your desired query

        while True:
            # Search Shodan API and send results to Kafka
            search_shodan_and_send(bootstrap_servers, topic, query, api_key)
            time.sleep(60)  # Sleep for 60 seconds before making the next query
    else:
        print("Please provide Kafka connection details via environment variables: KAFKA_BOOTSTRAP_SERVERS, KAFKA_TOPIC, and SHODAN_API_KEY")