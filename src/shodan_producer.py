# Shodan Producer Main.py
#
# Handler for the Shodan Producer container
# - Loads the environment variables
#   - Handles .env location
#   - Handles missing environment variables
# - Connects to Shodan API
# - Runs specified Queries
# TODO:  - Loads the queries
# TODO:  - Handles failures of queries
# TODO:- Dispatches the results to Kafka topic
# TODO:- Continually runs on a specified interval

from lib.shodan_util import shodanAPI
from lib.kafka_util import KafkaConnection
from lib.env_util import get_env_variable

from datetime import datetime
import time


def main():
    print("Gathering ENVs")
    shodan_api_key = get_env_variable("SHODAN_API_KEY")
    asn = get_env_variable("ASN")
    kafka_connection = get_env_variable("KAFKA_CONNECTION")

    print("Connecting to Shodan.io")
    api = shodanAPI(shodan_api_key)

    print("Connecting to Kafka")
    producer = KafkaConnection(kafka_connection, 'shodan-asn-count')

    print("Starting send loop")

    while True:
        time.sleep(5)
        print("Sending")
        producer.send(value=api.raw_query(f'asn:{asn}'))
            
# Only run in main
if __name__ == "__main__":
    main()
