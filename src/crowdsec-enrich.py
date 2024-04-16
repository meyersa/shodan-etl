# Enriches IP Information with Crowdsec
# TODO: Subscribe to Kafka Consumer
# TODO: Read data
# TODO: Interface with Crowdsec LAPI
# TODO: Subscribe to Kafka Producer
# TODO: Push data

from lib.kafka_util import KafkaConnection
from lib.env_util import get_env_variable
import time

def main():
    print("Gathering ENVs")
    kafka_connection = get_env_variable("KAFKA_CONNECTION")

    print("Connecting to Kafka")
    Consumer = KafkaConnection(kafka_connection, 'shodan-asn-count')

    print("Starting loop")
    while True: 
        time.sleep(5)

        print("Polling")
        msg = Consumer.poll_message()

        if msg is None: 
            continue

        print(msg) 



        

# Only run in main
if __name__ == "__main__":
    main()
