# Shodan Producer Main.py
#
# Handler for the Shodan Producer container
# - Loads the environment variables
#   - Handles .env location
#   - Handles missing environment variables
# - Connects to Shodan API
# - Runs specified Queries

from lib.shodan_util import shodanAPI
from lib.kafka_util import KafkaConnection
from lib.env_util import get_env_variable
import time

def main():
    print("Gathering ENVs")
    shodan_api_key = get_env_variable("SHODAN_API_KEY")
    kafka_connection = get_env_variable("KAFKA_CONNECTION")
    
    print("Connecting to Shodan.io")
    api = shodanAPI(shodan_api_key)

    print("Connecting to Kafka")
    producer = KafkaConnection(kafka_connection, 'shodan-producer')

    print("Starting send loop")

    while True:
        print("Sending")
                    
        try:
            result = api.raw_query(f'CMICH')

            for res in result: 
                producer.send(value=res)
                time.sleep(5)
                
            print("Sent")
            
        except ValueError: 
            print("Failed to send: ran into an error querying the Shodan API.. Continuing")

        time.sleep(60)
            
# Only run in main
if __name__ == "__main__":
    main()