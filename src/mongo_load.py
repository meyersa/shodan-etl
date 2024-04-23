from lib.kafka_util import KafkaConnection
from lib.env_util import get_env_variable
import time
from pymongo import MongoClient


def main():
    print("Gathering ENVs")
    kafka_connection = get_env_variable("KAFKA_CONNECTION")
    mongo_db = get_env_variable("MONGO_DB")
    mongo_user = get_env_variable("MONGO_INITDB_ROOT_USERNAME")
    mongo_password = get_env_variable("MONGO_INITDB_ROOT_PASSWORD")

    # Start delay
    delay = int(get_env_variable("DELAY"))
    time.sleep(delay)

    print("Connecting to Kafka")
    Consumer = KafkaConnection(kafka_connection, "enriched")

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

        results: dict
        ip = results.get("ip_str")

        # Query Mongo For incoming IP
        existing_record = collection.find_one({"ip": ip})

        # If there is no result
        if existing_record is None:
            collection.insert_one(results)

        # If the record is not the same
        if existing_record != results:
            collection.replace_one({"ip": ip}, results)


# Only run in main
if __name__ == "__main__":
    main()
