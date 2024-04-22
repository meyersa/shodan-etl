# Subscribe to Kafka 
# Watch for new entries
# Standardize data
# Send to processed topic

from lib.kafka_util import KafkaConnection
from lib.env_util import get_env_variable
import time
import json
from pymongo import MongoClient 

def main():
    print("Gathering ENVs")
    kafka_connection = get_env_variable("KAFKA_CONNECTION")
    mongo_db = get_env_variable("MONGO_DB")
    mongo_user = get_env_variable("MONGO_INITDB_ROOT_USERNAME")
    mongo_password = get_env_variable("MONGO_INITDB_ROOT_PASSWORD")
    
    print("Connecting to Kafka")
    Consumer = KafkaConnection(kafka_connection, 'enriched')
    Producer = KafkaConnection(kafka_connection, 'loaded')

    print("Connecting to MongoDB")
    mongo_client = MongoClient(
        "mongodb",
        username=mongo_user,
        password=mongo_password,
    )
    db = mongo_client[mongo_db]
    collection = db["ip-information"]

    print("Starting loop")
    while True: 
        results = Consumer.poll_message()
        
        if results is None: 
            continue
        
        results:dict
        ip = results.get("ip_str")

        # Query Mongo For incoming IP 
        existing_record = collection.find_one({"ip": ip})

        if existing_record: 
            collection.replace_one({"ip": ip}, results)
            
        else: 
            collection.insert_one(results)
            
# Only run in main
if __name__ == "__main__":
    main()
